from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Category, Product
from .forms import CategoryForm, ProductForm


@login_required
def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "catalog/category_list.html", {
        "categories": categories
    })


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/catalog/categories/")
    else:
        form = CategoryForm()

    return render(request, "catalog/category_form.html", {
        "form": form,
        "page_title": "Add Category"
    })


@login_required
def product_list(request):
    products = Product.objects.select_related("category").all().order_by("name")
    return render(request, "catalog/product_list.html", {
        "products": products
    })


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/catalog/products/")
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {
        "form": form,
        "page_title": "Add Product"
    })


@login_required
def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("/catalog/categories/")
    else:
        form = CategoryForm(instance=category)

    return render(request, "catalog/category_form.html", {
        "form": form,
        "page_title": "Edit Category"
    })


@login_required
def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("/catalog/products/")
    else:
        form = ProductForm(instance=product)

    return render(request, "catalog/product_form.html", {
        "form": form,
        "page_title": "Edit Product",
        "product": product,
    })


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