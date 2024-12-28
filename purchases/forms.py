from django import forms
from .models import Invoice, InvoiceItem
from input.models import Items
from configrate.models import Store
from purchases.models import Supplier
from TaxApp.models import Tax
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'supplier', 'supplier_invoice_number', 'supplier_invoice_date',
            'store', 'payment_method', 'discount_type', 'discount_value', 'tax_value'
        ]
        widgets = {
            'supplier_invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'discount_value': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'tax_value': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }

    def clean_supplier_invoice_date(self):
        # التحقق من أن تاريخ الفاتورة ليس في المستقبل
        date = self.cleaned_data['supplier_invoice_date']
        if date > date.today():
            raise ValidationError("تاريخ فاتورة المورد لا يمكن أن يكون في المستقبل.")
        return date

    def clean_tax_value(self):
        # التحقق من أن قيمة الضريبة بين 0 و 100%
        tax_value = self.cleaned_data.get('tax_value', 0)
        if tax_value < 0:
            raise ValidationError("قيمة الضريبة لا يمكن أن تكون أقل من 0.")
        if tax_value > 100:
            raise ValidationError("قيمة الضريبة لا يمكن أن تتجاوز 100%.")
        return tax_value

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['item', 'quantity', 'purchase_price', 'selling_price', 'discount']
        widgets = {
            'purchase_price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'selling_price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'discount': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        purchase_price = cleaned_data.get('purchase_price')
        selling_price = cleaned_data.get('selling_price')
        discount = cleaned_data.get('discount')

        # التحقق من صحة الكمية وسعر الشراء وسعر البيع والخصم
        if quantity <= 0:
            raise ValidationError("الكمية يجب أن تكون أكبر من 0.")
        if purchase_price <= 0:
            raise ValidationError("سعر الشراء يجب أن يكون أكبر من 0.")
        if selling_price <= 0:
            raise ValidationError("سعر البيع يجب أن يكون أكبر من 0.")
        if discount < 0:
            raise ValidationError("الخصم لا يمكن أن يكون أقل من 0.")

        return cleaned_data
    
    