from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter(name="money")
def money(value):
    """Render a Decimal/number without a trailing '.00', keeping real decimals intact."""
    if value in (None, ""):
        return ""
    try:
        d = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value
    if d == d.to_integral_value():
        return str(int(d))
    normalized = d.normalize()
    return f"{normalized:f}"
