from decimal import Decimal
from django.db.models import Sum
from catalog.models import Product
from orders.models import OrderItem


def build_abc_report():
    """
    Returns list of rows with:
    product, qty_sold, sales_value, cumulative_pct, abc_class
    """
    # total qty sold per product (only CONFIRMED orders)
    qs = (
        OrderItem.objects
        .filter(order__status="CONFIRMED")
        .values("product")
        .annotate(qty_sold=Sum("quantity"))
    )

    qty_map = {row["product"]: row["qty_sold"] or 0 for row in qs}

    rows = []
    total_value = Decimal("0")

    for p in Product.objects.all():
        qty = int(qty_map.get(p.id, 0))
        value = (Decimal(qty) * (p.selling_price or Decimal("0"))).quantize(Decimal("0.01"))
        rows.append({
            "product": p,
            "qty_sold": qty,
            "sales_value": value,
        })
        total_value += value

    # sort by sales value desc
    rows.sort(key=lambda r: r["sales_value"], reverse=True)

    # cumulative % and class
    running = Decimal("0")
    for r in rows:
        running += r["sales_value"]
        if total_value > 0:
            cumulative_pct = (running / total_value) * Decimal("100")
        else:
            cumulative_pct = Decimal("0")

        # ABC thresholds
        if cumulative_pct <= 70:
            abc_class = "A"
        elif cumulative_pct <= 90:
            abc_class = "B"
        else:
            abc_class = "C"

        r["cumulative_pct"] = cumulative_pct.quantize(Decimal("0.01"))
        r["abc_class"] = abc_class

    return rows, total_value.quantize(Decimal("0.01"))