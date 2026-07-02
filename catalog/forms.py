from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        qs = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"A category named '{name}' already exists.")
        return name


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "selling_price",
            "unit_cost",
            "annual_demand",
            "ordering_cost",
            "holding_cost",
            "current_stock",
            "reorder_point",
            "image",
        ]
        widgets = {
            "selling_price": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
            "unit_cost": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
            "annual_demand": forms.NumberInput(attrs={"min": "0"}),
            "ordering_cost": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "holding_cost": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "current_stock": forms.NumberInput(attrs={"min": "0"}),
            "reorder_point": forms.NumberInput(attrs={"min": "0"}),
        }
        help_texts = {
            "ordering_cost": "The cost of placing one purchase order for this product (paperwork, delivery, etc.) — used to calculate the recommended reorder quantity.",
            "holding_cost": "The cost of storing one unit of this product for a year (space, insurance, risk of damage) — used to calculate the recommended reorder quantity.",
            "annual_demand": "How many units you expect to sell in a year. If you leave this as 0, the system will use your real order history instead once you have 12 months of sales data.",
            "reorder_point": "When stock falls below this number, the product is flagged as low stock.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_categories = Category.objects.filter(is_active=True)
        if self.instance.pk and self.instance.category_id:
            self.fields["category"].queryset = (
                active_categories | Category.objects.filter(pk=self.instance.category_id)
            ).distinct()
        else:
            self.fields["category"].queryset = active_categories

    def clean_name(self):
        name = self.cleaned_data["name"]
        qs = Product.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"A product named '{name}' already exists.")
        return name
