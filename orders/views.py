from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.audit import log_action
from .bill import generate_bill_pdf
from .models import Customer, Invoice, Order, OrderItem
from .forms import BillDetailsForm, CustomerForm, OrderItemFormSet, OrderReturnForm
from .services import cancel_order, confirm_order, process_return


@login_required
def order_list(request):
    orders = Order.objects.select_related("created_by", "customer").prefetch_related("items__product").order_by("-id")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_create(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer") or None
        reset_formset = False

        with transaction.atomic():
            order = Order.objects.create(created_by=request.user, customer_id=customer_id)
            formset = OrderItemFormSet(request.POST, instance=order)
            success = False

            if formset.is_valid():
                items = formset.save(commit=False)

                valid_items = 0
                for item in items:
                    if item.product and item.quantity:
                        item.order = order
                        item.save()
                        valid_items += 1

                for deleted_item in formset.deleted_objects:
                    deleted_item.delete()

                if valid_items > 0:
                    success = True
                else:
                    messages.error(request, "Please add at least one valid order item.")
                    reset_formset = True
            else:
                messages.error(request, "Please fix the errors below.")

            if not success:
                order.delete()

        if success:
            log_action(request.user, "CREATE", order)
            return redirect(f"/orders/{order.id}/")

        if reset_formset:
            formset = OrderItemFormSet()

        return render(request, "orders/order_form.html", {
            "formset": formset,
            "customers": Customer.objects.order_by("name"),
            "page_title": "Create Order",
        })

    formset = OrderItemFormSet()
    return render(request, "orders/order_form.html", {
        "formset": formset,
        "customers": Customer.objects.order_by("name"),
        "page_title": "Create Order",
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("created_by", "customer").prefetch_related(
            "items__product", "status_logs__changed_by",
            "returns__product", "returns__processed_by",
            "invoices__issued_by",
        ),
        id=order_id,
    )
    return_form = OrderReturnForm() if order.status == "CONFIRMED" else None
    return render(request, "orders/order_detail.html", {
        "order": order,
        "return_form": return_form,
    })


@login_required
@require_POST
def order_confirm_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        confirm_order(order, changed_by=request.user)
        log_action(request.user, "UPDATE", order, "DRAFT → CONFIRMED")
        messages.success(request, f"Order #{order.id} confirmed successfully.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect(f"/orders/{order.id}/")


@login_required
@require_POST
def order_cancel_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        cancel_order(order, changed_by=request.user, note=request.POST.get("note", ""))
        log_action(request.user, "UPDATE", order, "DRAFT → CANCELLED")
        messages.success(request, f"Order #{order.id} has been cancelled.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect(f"/orders/{order.id}/")


@login_required
@require_POST
def order_return_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderReturnForm(request.POST)
    if form.is_valid():
        try:
            ret = process_return(
                order=order,
                product=form.cleaned_data["product"],
                quantity=form.cleaned_data["quantity"],
                reason=form.cleaned_data["reason"],
                processed_by=request.user,
            )
            log_action(request.user, "CREATE", ret)
            messages.success(request, f"Return processed: {ret.product.name} x {ret.quantity} added back to stock.")
        except ValueError as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "Invalid return details.")
    return redirect(f"/orders/{order.id}/")


# ── Bill / Tax Invoice ──────────────────────────────────────────────────────

@login_required
def bill_view(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('customer', 'created_by').prefetch_related('items__product'),
        id=order_id, status='CONFIRMED',
    )
    today = timezone.localdate()
    if request.method == 'POST':
        form = BillDetailsForm(request.POST, order=order)
        if form.is_valid():
            invoice = Invoice.objects.create(
                order=order,
                invoice_no=form.cleaned_data['invoice_no'],
                bill_date=form.cleaned_data['bill_date'],
                transaction_date=form.cleaned_data['transaction_date'],
                payment_mode=form.cleaned_data['payment_mode'],
                discount=form.cleaned_data['discount'],
                staff_name=form.cleaned_data['staff_name'],
                issued_by=request.user,
            )
            pdf_bytes = generate_bill_pdf(
                order=order,
                invoice_no=invoice.invoice_no,
                bill_date=invoice.bill_date,
                transaction_date=invoice.transaction_date,
                payment_mode=invoice.payment_mode,
                discount=invoice.discount,
                staff_name=invoice.staff_name,
            )
            resp = HttpResponse(pdf_bytes, content_type='application/pdf')
            resp['Content-Disposition'] = f'inline; filename="invoice_{invoice.invoice_no}.pdf"'
            return resp
    else:
        form = BillDetailsForm(order=order, initial={
            'bill_date': today,
            'transaction_date': timezone.localtime(order.created_at).date(),
            'staff_name': order.created_by.get_full_name() or order.created_by.username,
        })
    existing_invoices = order.invoices.select_related('issued_by').order_by('-issued_at')
    return render(request, 'orders/bill_form.html', {
        'order': order,
        'form': form,
        'existing_invoices': existing_invoices,
    })


@login_required
def invoice_download_view(request, invoice_id):
    invoice = get_object_or_404(
        Invoice.objects.select_related(
            'order__customer', 'order__created_by'
        ).prefetch_related('order__items__product'),
        id=invoice_id,
    )
    pdf_bytes = generate_bill_pdf(
        order=invoice.order,
        invoice_no=invoice.invoice_no,
        bill_date=invoice.bill_date,
        transaction_date=invoice.transaction_date,
        payment_mode=invoice.payment_mode,
        discount=invoice.discount,
        staff_name=invoice.staff_name,
    )
    resp = HttpResponse(pdf_bytes, content_type='application/pdf')
    resp['Content-Disposition'] = f'inline; filename="invoice_{invoice.invoice_no}.pdf"'
    return resp


# ── Customer views ──────────────────────────────────────────────────────────

@login_required
def customer_list(request):
    customers = Customer.objects.order_by("name")
    return render(request, "orders/customer_list.html", {"customers": customers})


@login_required
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            log_action(request.user, "CREATE", customer)
            return redirect("/orders/customers/")
    else:
        form = CustomerForm()
    return render(request, "orders/customer_form.html", {"form": form, "page_title": "Add Customer"})


@login_required
def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            log_action(request.user, "UPDATE", customer)
            return redirect("/orders/customers/")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "orders/customer_form.html", {"form": form, "page_title": "Edit Customer", "customer": customer})