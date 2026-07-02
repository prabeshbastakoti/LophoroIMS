from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image

name_format_validator = RegexValidator(
    regex=r"^[A-Za-z0-9][A-Za-z0-9 \-_.,'&()]*$",
    message="Name must start with a letter or number, and may only contain letters, numbers, spaces, and - _ . , ' & ( )",
)


def validate_name_has_letter(value):
    if not any(ch.isalpha() for ch in value):
        raise ValidationError("Name must contain at least one letter.")


MAX_IMAGE_UPLOAD_BYTES = 5 * 1024 * 1024


def validate_image_upload_size(file):
    if file.size > MAX_IMAGE_UPLOAD_BYTES:
        raise ValidationError("Image is too large — please use a photo under 5MB.")


class Category(models.Model):
    name = models.CharField(max_length=100, validators=[name_format_validator, validate_name_has_letter])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


MAX_IMAGE_SIZE = (1000, 1000)
IMAGE_QUALITY = 85


class Product(models.Model):
    name = models.CharField(max_length=200, validators=[name_format_validator, validate_name_has_letter])
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01, message="Selling price must be greater than 0.")],
    )
    unit_cost = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01, message="Unit cost must be greater than 0.")],
    )

    annual_demand = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Annual demand cannot be negative.")],
    )
    ordering_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0, message="Ordering cost cannot be negative.")],
    )
    holding_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0, message="Holding cost cannot be negative.")],
    )

    current_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Current stock cannot be negative.")],
    )
    reorder_point = models.PositiveIntegerField(
        default=10,
        help_text="Stock level at which this product should be flagged as low/reorder-needed.",
    )
    image = models.ImageField(
        upload_to="products/", blank=True, null=True,
        validators=[validate_image_upload_size],
    )

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
