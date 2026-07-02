from django.db import transaction
from django.db.models import Sum
from inventory.services import stock_in, stock_out
from .models import Order, OrderReturn, OrderStatusLog


@transaction.atomic
def confirm_order(order: Order, changed_by=None) -> Order:
    if order.status != "DRAFT":
        raise ValueError("Only DRAFT orders can be confirmed")

    for item in order.items.select_related("product").all():
        stock_out(item.product, item.quantity)

    old_status = order.status
    order.status = "CONFIRMED"
    order.save(update_fields=["status"])
    OrderStatusLog.objects.create(order=order, old_status=old_status, new_status="CONFIRMED", changed_by=changed_by)
    return order


@transaction.atomic
def cancel_order(order: Order, changed_by=None, note="") -> Order:
    if order.status != "DRAFT":
        raise ValueError("Only DRAFT orders can be cancelled")

    old_status = order.status
    order.status = "CANCELLED"
    order.save(update_fields=["status"])
    OrderStatusLog.objects.create(order=order, old_status=old_status, new_status="CANCELLED", changed_by=changed_by, note=note)
    return order


@transaction.atomic
def process_return(order: Order, product, quantity: int, reason: str, processed_by=None) -> OrderReturn:
    if order.status != "CONFIRMED":
        raise ValueError("Returns can only be processed for confirmed orders")

    ordered_qty = order.items.filter(product=product).aggregate(total=Sum("quantity"))["total"] or 0
    returned_qty = order.returns.filter(product=product).aggregate(total=Sum("quantity"))["total"] or 0
    remaining = ordered_qty - returned_qty
    if quantity > remaining:
        raise ValueError(
            f"Cannot return {quantity} unit(s) of {product.name} — only {remaining} unit(s) remain eligible for return."
        )

    stock_in(product, quantity)
    return OrderReturn.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        reason=reason,
        processed_by=processed_by,
    )