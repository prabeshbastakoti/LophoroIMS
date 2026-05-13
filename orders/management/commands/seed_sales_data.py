import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Product
from orders.models import Order, OrderItem

User = get_user_model()

# Realistic monthly revenue targets (NPR) for a decor store
# Slightly rising trend with a dip in Jan — mirrors typical seasonal behaviour
MONTHLY_TARGETS = [
    ("2025-11", 180_000),
    ("2025-12", 240_000),
    ("2026-01", 160_000),
    ("2026-02", 210_000),
    ("2026-03", 275_000),
    ("2026-04", 230_000),
]


class Command(BaseCommand):
    help = "Seed dummy sales data across 6 past months for demo purposes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove previously seeded dummy orders before seeding",
        )

    def handle(self, *args, **options):
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR(
                "No products found. Add at least one product first."
            ))
            return

        admin = User.objects.filter(role="ADMIN").first() or User.objects.first()
        if not admin:
            self.stdout.write(self.style.ERROR("No users found."))
            return

        if options["clear"]:
            deleted, _ = Order.objects.filter(
                is_seed_data=True
            ).delete() if hasattr(Order, "is_seed_data") else (0, {})
            # Fall back: delete orders that have the seed marker in their note
            deleted = Order.objects.filter(
                status_logs__note="[seed]"
            ).distinct().delete()[0]
            self.stdout.write(f"Removed {deleted} seeded orders.")

        created_count = 0

        for month_str, target_revenue in MONTHLY_TARGETS:
            year, month = map(int, month_str.split("-"))

            # Skip months that already have confirmed order data
            from django.db.models.functions import TruncMonth
            from django.db.models import Sum
            existing = (
                OrderItem.objects
                .filter(order__status="CONFIRMED")
                .annotate(m=TruncMonth("order__created_at"))
                .filter(m__year=year, m__month=month)
                .aggregate(total=Sum("quantity"))["total"] or 0
            )
            if existing > 0:
                self.stdout.write(f"  {month_str}: skipped (already has data)")
                continue

            # Build orders that together hit roughly the target revenue
            revenue_so_far = 0
            orders_this_month = 0

            while revenue_so_far < target_revenue:
                # Pick 1–4 random products for this order
                batch = random.sample(products, min(random.randint(1, 4), len(products)))

                # Random day within the month
                day = random.randint(1, 27)
                hour = random.randint(9, 18)
                order_date = timezone.datetime(year, month, day, hour, 0, 0,
                                               tzinfo=timezone.get_current_timezone())

                order = Order.objects.create(
                    created_by=admin,
                    status="CONFIRMED",
                )
                # Backdate created_at — update() bypasses auto_now_add
                Order.objects.filter(id=order.id).update(created_at=order_date)

                order_revenue = 0
                for product in batch:
                    qty = random.randint(1, 5)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=qty,
                    )
                    order_revenue += qty * float(product.selling_price)

                revenue_so_far += order_revenue
                orders_this_month += 1
                created_count += 1

                # Cap at 8 orders per month to avoid runaway loop on low-priced products
                if orders_this_month >= 8:
                    break

            self.stdout.write(
                self.style.SUCCESS(
                    f"  {month_str}: {orders_this_month} orders, "
                    f"~NPR {revenue_so_far:,.0f} revenue"
                )
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created {created_count} dummy orders. "
            f"Reload the Sales Trends page to see the line graph."
        ))
