from django.db import transaction
from catalog.models import Product
from .models import StockMovement


@transaction.atomic
def stock_in(product: Product, qty: int) -> StockMovement:
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")

    movement = StockMovement.objects.create(
        product=product,
        movement_type="IN",
        quantity=qty,
    )

    product.current_stock += qty
    product.save(update_fields=["current_stock"])

    return movement


@transaction.atomic
def stock_out(product: Product, qty: int) -> StockMovement:
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")

    if product.current_stock < qty:
        raise ValueError("Not enough stock")

    movement = StockMovement.objects.create(
        product=product,
        movement_type="OUT",
        quantity=qty,
    )

    product.current_stock -= qty
    product.save(update_fields=["current_stock"])

    return movement