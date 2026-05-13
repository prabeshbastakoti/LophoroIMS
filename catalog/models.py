from django.db import models
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


MAX_IMAGE_SIZE = (1000, 1000)
IMAGE_QUALITY = 85


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    annual_demand = models.IntegerField(default=0)
    ordering_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    current_stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._resize_image()

    def _resize_image(self):
        try:
            img = Image.open(self.image.path)
            if img.width > MAX_IMAGE_SIZE[0] or img.height > MAX_IMAGE_SIZE[1]:
                img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(self.image.path, format="JPEG", quality=IMAGE_QUALITY, optimize=True)
        except Exception:
            pass
