from django.db import models
from catalog.models import Product


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"