from django import forms
from .models import PurchaseInvoice, InvoiceDetail
from purchases.Supplier.models import Supplier
from configrate.models import Store, Unit
from input.models import Items
from TaxApp.models import Tax
from django.utils.translation import gettext_lazy as _


class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = PurchaseInvoice
        fields = ['date', 'supplier', 'supplier_invoice_number', 'supplier_invoice_date', 'store', 'payment_method', 'discount_type', 'discount_value', 'tax_value']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'supplier_invoice_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # لإظهار رصيد المورد بعد اختياره
    supplier_balance = forms.DecimalField(required=False, disabled=True, label=_("رصيد المورد"), initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # تأكد من أن المورد موجود
        if self.instance and self.instance.supplier:
            self.fields['supplier_balance'].initial = self.instance.supplier.balance
        else:
            self.fields['supplier_balance'].initial = 0  # تعيين رصيد المورد إلى 0 إذا لم يتم تحديده
            self.fields['supplier'].required = True  # تأكد من أن المورد مطلوب في هذه الحالة

    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')
        if supplier:
            # إذا تم تحديد المورد، قم بتحديث الرصيد
            self.fields['supplier_balance'].initial = supplier.balance
        else:
            # إذا لم يتم تحديد المورد، تأكد من أن الرصيد لا يظهر
            self.fields['supplier_balance'].initial = 0
        return supplier

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ['Items', 'unit', 'quantity', 'price', 'discount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.all()  # لاختيار الوحدات المتاحة
        self.fields['Items'].queryset = Items.objects.all()  # لاختيار الأصناف المتاحة

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier  # تحديد نموذج Supplier
        fields = ['name_lo', 'name_fk', 'VatNumber', 'TelPhone', 'phone', 'Address', 'balance', 'is_stop']
