from collections import OrderedDict
from decimal import Decimal
from django.db.models.functions import TruncMonth

from orders.models import OrderItem


def build_sales_trend():
    """
    Returns list of rows:
    month_label, revenue, growth_pct
    """
    items = (
        OrderItem.objects
        .filter(order__status="CONFIRMED")
        .select_related("product")
        .annotate(month=TruncMonth("order__created_at"))
        .order_by("month")
    )

    revenue_by_month = OrderedDict()

    for it in items:
        month = it.month
        if month not in revenue_by_month:
            revenue_by_month[month] = Decimal("0")
        revenue_by_month[month] += (Decimal(it.quantity) * it.product.selling_price)

    rows = []
    prev_rev = None

    for month, rev in revenue_by_month.items():
        rev = rev.quantize(Decimal("0.01"))
        if prev_rev is None or prev_rev == 0:
            growth = None
        else:
            growth = ((rev - prev_rev) / prev_rev) * Decimal("100")
            growth = growth.quantize(Decimal("0.01"))

        rows.append({
            "month": month.strftime("%Y-%m"),
            "revenue": rev,
            "growth": growth,  # None for first month
        })
        prev_rev = rev

    return rows