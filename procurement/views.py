from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from accounts.audit import log_action
from .models import Supplier, Purchase, SupplierPriceHistory
from .forms import SupplierForm, PurchaseItemFormSet
from .services import receive_purchase


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/login/")
        if request.user.role != "ADMIN":
            return HttpResponseForbidden("Access denied. Only admin can access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("name")
    return render(request, "procurement/supplier_list.html", {
        "suppliers": suppliers
    })


@login_required
@admin_required
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
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

        purchase = Purchase.objects.create(
            supplier_id=supplier_id,
            created_by=request.user
        )

        formset = PurchaseItemFormSet(request.POST, instance=purchase)

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

            if valid_items == 0:
                purchase.delete()
                messages.error(request, "Please add at least one valid purchase item.")
                return redirect("/procurement/purchases/add/")

            return redirect(f"/procurement/purchases/{purchase.id}/")

        purchase.delete()

    formset = PurchaseItemFormSet()
    suppliers = Supplier.objects.all().order_by("name")

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
def purchase_receive_view(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    try:
        receive_purchase(purchase, received_by=request.user)
        log_action(request.user, "UPDATE", purchase, "DRAFT → RECEIVED")
        messages.success(request, f"Purchase #{purchase.id} received successfully.")
    except Exception as e:
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