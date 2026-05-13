from django.db import transaction
from inventory.services import stock_in
from .models import Purchase, SupplierPriceHistory


@transaction.atomic
def receive_purchase(purchase: Purchase, received_by=None) -> Purchase:
    if purchase.status != "DRAFT":
        raise ValueError("Only DRAFT purchases can be received")

    for item in purchase.items.select_related("product").all():
        stock_in(item.product, item.quantity)
        SupplierPriceHistory.objects.create(
            supplier=purchase.supplier,
            product=item.product,
            unit_cost=item.unit_cost,
            recorded_by=received_by,
        )

    purchase.status = "RECEIVED"
    purchase.save(update_fields=["status"])
    return purchase