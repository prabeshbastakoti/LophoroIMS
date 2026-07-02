from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render

from catalog.models import Product
from .models import StockMovement


@login_required
def stock_movement_list(request):
    movements = StockMovement.objects.select_related("product").order_by("-created_at")
    return render(request, "inventory/stock_movement_list.html", {
        "movements": movements
    })


@login_required
def current_stock(request):
    products = Product.objects.select_related("category").order_by("name")
    low_stock = products.filter(current_stock__lt=F("reorder_point"))
    return render(request, "inventory/current_stock.html", {
        "products": products,
        "low_stock": low_stock,
    })
