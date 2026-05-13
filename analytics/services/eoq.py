import math
from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from catalog.models import Product
from orders.models import OrderItem


def get_annual_demand(product: Product) -> tuple:
    """
    Returns (demand: int, source: str).
    Tries real order history first (last 365 days of confirmed orders).
    Falls back to the manually-entered product.annual_demand if no sales data.
    source is one of: 'orders' | 'manual' | 'none'
    """
    cutoff = timezone.now() - timedelta(days=365)
    result = (
        OrderItem.objects
        .filter(
            order__status='CONFIRMED',
            order__created_at__gte=cutoff,
            product=product,
        )
        .aggregate(total=Sum('quantity'))
    )
    total = result['total'] or 0
    if total > 0:
        return total, 'orders'
    if product.annual_demand > 0:
        return product.annual_demand, 'manual'
    return 0, 'none'


def calculate_eoq(product: Product, annual_demand: int = None):
    D = annual_demand if annual_demand is not None else product.annual_demand
    S = float(product.ordering_cost)
    H = float(product.holding_cost)

    if D <= 0 or S <= 0 or H <= 0:
        return None

    return round(math.sqrt((2 * D * S) / H), 2)
