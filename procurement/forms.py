from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from catalog.models import Product
from .models import Supplier, Purchase, PurchaseItem


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "phone", "email", "address"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        qs = Supplier.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"A supplier named '{name}' already exists.")
        return name


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "unit_cost"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"min": "1"}),
            "unit_cost": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_products = Product.objects.filter(is_active=True)
        if self.instance.pk and self.instance.product_id:
            self.fields["product"].queryset = (
                active_products | Product.objects.filter(pk=self.instance.product_id)
            ).distinct()
        else:
            self.fields["product"].queryset = active_products


class BasePurchaseItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        seen = set()
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or form.cleaned_data.get("DELETE"):
                continue
            product = form.cleaned_data.get("product")
            if product:
                if product.id in seen:
                    raise forms.ValidationError(
                        f"Product '{product.name}' is listed more than once — please combine into a single line."
                    )
                seen.add(product.id)


PurchaseItemFormSet = inlineformset_factory(
    Purchase,
    PurchaseItem,
    form=PurchaseItemForm,
    formset=BasePurchaseItemFormSet,
    extra=1,
    can_delete=True
)
