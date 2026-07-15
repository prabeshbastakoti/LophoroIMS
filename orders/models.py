from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from catalog.models import Product
from lophoroims.validators import pan_validator, phone_validator


class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True, validators=[phone_validator])
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    buyer_pan = models.CharField(
        max_length=9, blank=True, verbose_name="PAN No.", validators=[pan_validator],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    )

    SOURCE_CHOICES = (
        ("INSTAGRAM", "Instagram"),
        ("FACEBOOK", "Facebook"),
        ("WHATSAPP", "WhatsApp"),
        ("FRIEND_FAMILY", "Friend/Family"),
        ("OTHER", "Other"),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="DRAFT")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1, message="Quantity must be at least 1.")])

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name} x {self.quantity}"


class OrderStatusLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_logs")
    old_status = models.CharField(max_length=10)
    new_status = models.CharField(max_length=10)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.order.id}: {self.old_status} → {self.new_status}"


class OrderReturn(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="returns")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1, message="Quantity must be at least 1.")])
    reason = models.TextField(blank=True)
    returned_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Return for Order #{self.order.id} - {self.product.name} x {self.quantity}"


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="invoices")
    invoice_no = models.CharField(max_length=30, unique=True)
    bill_date = models.DateField()
    transaction_date = models.DateField()
    payment_mode = models.CharField(max_length=20)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0, message="Discount cannot be negative.")],
    )
    staff_name = models.CharField(max_length=100)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="issued_invoices"
    )
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self):
        return f"Invoice #{self.invoice_no} — Order #{self.order.id}"