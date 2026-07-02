from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.audit import log_action
from .models import Category, Product
from .forms import CategoryForm, ProductForm


@login_required
def category_list(request):
    show_inactive = request.GET.get("show") == "inactive"
    categories = Category.objects.filter(is_active=not show_inactive).order_by("name")
    return render(request, "catalog/category_list.html", {
        "categories": categories,
        "show_inactive": show_inactive,
    })


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            log_action(request.user, "CREATE", category)
            return redirect("/catalog/categories/")
    else:
        form = CategoryForm()

    return render(request, "catalog/category_form.html", {
        "form": form,
        "page_title": "Add Category"
    })


@login_required
def product_list(request):
    show_inactive = request.GET.get("show") == "inactive"
    products = Product.objects.select_related("category").filter(is_active=not show_inactive).order_by("name")
    return render(request, "catalog/product_list.html", {
        "products": products,
        "show_inactive": show_inactive,
    })


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            log_action(request.user, "CREATE", product)
            return redirect("/catalog/products/")
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {
        "form": form,
        "page_title": "Add Product"
    })


@login_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            log_action(request.user, "UPDATE", category)
            return redirect("/catalog/categories/")
    else:
        form = CategoryForm(instance=category)

    return render(request, "catalog/category_form.html", {
        "form": form,
        "page_title": "Edit Category"
    })


@login_required
@require_POST
def category_toggle_active(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.is_active = not category.is_active
    category.save(update_fields=["is_active"])
    log_action(request.user, "UPDATE", category, "Reactivated" if category.is_active else "Deactivated")
    messages.success(
        request,
        f"Category '{category.name}' has been {'reactivated' if category.is_active else 'deactivated'}."
    )
    return redirect("/catalog/categories/")


@login_required
@require_POST
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if category.product_set.exists():
        messages.error(
            request,
            f"Cannot delete '{category.name}' — it still has {category.product_set.count()} product(s) in it. "
            "Move or delete those products first."
        )
    else:
        deleted_pk = category.pk
        try:
            category.delete()
        except ProtectedError:
            messages.error(request, f"Cannot delete '{category.name}' — it is still in use.")
        else:
            category.pk = deleted_pk
            log_action(request.user, "DELETE", category)
            messages.success(request, f"Category '{category.name}' has been deleted.")
    return redirect("/catalog/categories/")


@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            log_action(request.user, "UPDATE", product)
            return redirect("/catalog/products/")
    else:
        form = ProductForm(instance=product)

    return render(request, "catalog/product_form.html", {
        "form": form,
        "page_title": "Edit Product",
        "product": product,
    })


@login_required
@require_POST
def product_toggle_active(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = not product.is_active
    product.save(update_fields=["is_active"])
    log_action(request.user, "UPDATE", product, "Reactivated" if product.is_active else "Deactivated")
    messages.success(
        request,
        f"Product '{product.name}' has been {'reactivated' if product.is_active else 'deactivated'}."
    )
    return redirect("/catalog/products/")


@login_required
@require_POST
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    deleted_pk = product.pk
    try:
        product.delete()
    except ProtectedError:
        messages.error(
            request,
            f"Cannot delete '{product.name}' — it is referenced by existing orders, returns, purchases, "
            "or stock movement history. Deactivate it instead."
        )
    else:
        product.pk = deleted_pk
        log_action(request.user, "DELETE", product)
        messages.success(request, f"Product '{product.name}' has been deleted.")
    return redirect("/catalog/products/")


@login_required
def search(request):
    query = request.GET.get("q")

    products = []
    categories = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )

        categories = Category.objects.filter(
            name__icontains=query
        )

    return render(request, "catalog/search_results.html", {
        "query": query,
        "products": products,
        "categories": categories
    })
