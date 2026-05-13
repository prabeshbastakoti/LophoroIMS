from django.conf import settings
from django.db import models
from catalog.models import Product


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("RECEIVED", "Received"),
        ("CANCELLED", "Cancelled"),
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="purchases")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="purchases")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="DRAFT")

    def __str__(self):
        return f"Purchase #{self.id} - {self.status}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Purchase #{self.purchase.id} - {self.product.name} x {self.quantity}"


class SupplierPriceHistory(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="price_history")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_history")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.supplier.name} — {self.product.name} @ NPR {self.unit_cost}"