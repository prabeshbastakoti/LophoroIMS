from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.audit import log_action
from accounts.decorators import admin_required
from .models import Supplier, Purchase, SupplierPriceHistory
from .forms import SupplierForm, PurchaseItemFormSet
from .services import receive_purchase


@login_required
@admin_required
def supplier_list(request):
    show_inactive = request.GET.get("show") == "inactive"
    suppliers = Supplier.objects.filter(is_active=not show_inactive).order_by("name")
    return render(request, "procurement/supplier_list.html", {
        "suppliers": suppliers,
        "show_inactive": show_inactive,
    })


@login_required
@admin_required
@require_POST
def supplier_toggle_active(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.is_active = not supplier.is_active
    supplier.save(update_fields=["is_active"])
    log_action(request.user, "UPDATE", supplier, "Reactivated" if supplier.is_active else "Deactivated")
    messages.success(
        request,
        f"Supplier '{supplier.name}' has been {'reactivated' if supplier.is_active else 'deactivated'}."
    )
    return redirect("/procurement/suppliers/")


@login_required
@admin_required
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            log_action(request.user, "CREATE", supplier)
            return redirect("/procurement/suppliers/")
    else:
        form = SupplierForm()

    return render(request, "procurement/supplier_form.html", {
        "form": form,
        "page_title": "Add Supplier"
    })


@login_required
def purchase_list(request):
    purchases = Purchase.objects.select_related("supplier", "created_by").prefetch_related("items__product").order_by("-id")
    return render(request, "procurement/purchase_list.html", {
        "purchases": purchases
    })


@login_required
def purchase_create(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        if not supplier_id:
            messages.error(request, "Please select a supplier.")
            return redirect("/procurement/purchases/add/")

        reset_formset = False

        with transaction.atomic():
            purchase = Purchase.objects.create(
                supplier_id=supplier_id,
                created_by=request.user
            )
            formset = PurchaseItemFormSet(request.POST, instance=purchase)
            success = False

            if formset.is_valid():
                items = formset.save(commit=False)

                valid_items = 0
                for item in items:
                    if item.product and item.quantity:
                        item.purchase = purchase
                        item.save()
                        valid_items += 1

                for deleted_item in formset.deleted_objects:
                    deleted_item.delete()

                if valid_items > 0:
                    success = True
                else:
                    messages.error(request, "Please add at least one valid purchase item.")
                    reset_formset = True
            else:
                messages.error(request, "Please fix the errors below.")

            if not success:
                purchase.delete()

        if success:
            log_action(request.user, "CREATE", purchase)
            return redirect(f"/procurement/purchases/{purchase.id}/")

        if reset_formset:
            return redirect("/procurement/purchases/add/")

        return render(request, "procurement/purchase_form.html", {
            "formset": formset,
            "suppliers": Supplier.objects.filter(is_active=True).order_by("name"),
            "page_title": "Create Purchase"
        })

    formset = PurchaseItemFormSet()
    suppliers = Supplier.objects.filter(is_active=True).order_by("name")

    return render(request, "procurement/purchase_form.html", {
        "formset": formset,
        "suppliers": suppliers,
        "page_title": "Create Purchase"
    })


@login_required
def purchase_detail(request, purchase_id):
    purchase = get_object_or_404(
        Purchase.objects.select_related("supplier", "created_by").prefetch_related("items__product"),
        id=purchase_id
    )
    return render(request, "procurement/purchase_detail.html", {
        "purchase": purchase
    })


@login_required
@require_POST
def purchase_receive_view(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    try:
        receive_purchase(purchase, received_by=request.user)
        log_action(request.user, "UPDATE", purchase, "DRAFT → RECEIVED")
        messages.success(request, f"Purchase #{purchase.id} received successfully.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect(f"/procurement/purchases/{purchase.id}/")


@login_required
@admin_required
def supplier_price_history(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    history = SupplierPriceHistory.objects.filter(supplier=supplier).select_related("product", "recorded_by")
    return render(request, "procurement/supplier_price_history.html", {
        "supplier": supplier,
        "history": history,
    })
