from decimal import Decimal, ROUND_HALF_UP

from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.utils import timezone

from catalog.models import Product
from .models import Customer, Invoice, Order, OrderItem, OrderReturn


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "email", "address", "buyer_pan"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"min": "1"}),
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


class BaseOrderItemFormSet(BaseInlineFormSet):
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


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    formset=BaseOrderItemFormSet,
    extra=1,
    can_delete=True
)


class OrderReturnForm(forms.ModelForm):
    class Meta:
        model = OrderReturn
        fields = ["product", "quantity", "reason"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"min": "1"}),
        }


class BillDetailsForm(forms.Form):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Credit", "Credit"),
        ("COD", "Cash on Delivery"),
        ("QR", "QR Payment"),
        ("Other", "Other"),
    ]
    invoice_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "e.g. 001"}),
    )
    transaction_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        initial=timezone.now,
    )
    bill_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        initial=timezone.now,
    )
    payment_mode = forms.ChoiceField(choices=PAYMENT_CHOICES)
    discount_type = forms.ChoiceField(choices=Invoice.DISCOUNT_TYPE_CHOICES, initial="AMOUNT")
    discount_value = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={"step": "0.01", "placeholder": "0.00"}),
    )
    staff_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Staff member name"}),
    )

    def __init__(self, *args, order=None, **kwargs):
        self.order = order
        super().__init__(*args, **kwargs)

    def clean_invoice_no(self):
        inv_no = self.cleaned_data["invoice_no"]
        if Invoice.objects.filter(invoice_no=inv_no).exists():
            raise forms.ValidationError(
                f'Invoice #{inv_no} has already been issued. Choose a different number.'
            )
        return inv_no

    def clean(self):
        cleaned_data = super().clean()
        transaction_date = cleaned_data.get("transaction_date")
        bill_date = cleaned_data.get("bill_date")
        if transaction_date and bill_date and bill_date < transaction_date:
            self.add_error("bill_date", "Bill date cannot be before the transaction date.")

        discount_type = cleaned_data.get("discount_type")
        discount_value = cleaned_data.get("discount_value")
        if discount_value is not None and self.order is not None:
            subtotal = sum(
                (item.quantity * item.product.selling_price for item in self.order.items.all()),
                Decimal("0"),
            )
            if discount_type == "PERCENT":
                if discount_value > 100:
                    self.add_error("discount_value", "Percentage discount cannot exceed 100%.")
                    return cleaned_data
                resolved_discount = (subtotal * discount_value / Decimal("100")).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            else:
                resolved_discount = discount_value

            if resolved_discount > subtotal:
                self.add_error(
                    "discount_value",
                    f"Discount cannot be greater than the order total (NPR {subtotal})."
                )
            cleaned_data["resolved_discount"] = resolved_discount
        return cleaned_data
