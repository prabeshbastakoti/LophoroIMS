from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


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
            "image",
        ]