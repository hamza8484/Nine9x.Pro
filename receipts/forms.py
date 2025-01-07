from django import forms
from .models import Receipt,Payment
from sales.models import Customer
from purchases.models import Supplier
from django.contrib.auth.models import User


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['customer', 'user','amount_received', 'payment_method', 'receipt_date', 'notes']

    customer_balance = forms.DecimalField(disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'customer' in self.initial:
            customer = self.initial['customer']
            self.fields['customer_balance'].initial = customer.balance


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['supplier', 'user', 'amount_paid', 'payment_method', 'payment_date', 'notes']

    #supplier_balance = forms.DecimalField(disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'supplier' in self.initial:
            supplier = self.initial['supplier']
            self.fields['supplier_balance'].initial = supplier.balance
