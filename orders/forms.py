from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import Customer, Invoice, Order, OrderItem, OrderReturn


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "email", "address", "buyer_pan"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)


class OrderReturnForm(forms.ModelForm):
    class Meta:
        model = OrderReturn
        fields = ["product", "quantity", "reason"]


class BillDetailsForm(forms.Form):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Credit", "Credit"),
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
    discount = forms.DecimalField(
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

    def clean_invoice_no(self):
        inv_no = self.cleaned_data["invoice_no"]
        if Invoice.objects.filter(invoice_no=inv_no).exists():
            raise forms.ValidationError(
                f'Invoice #{inv_no} has already been issued. Choose a different number.'
            )
        return inv_no