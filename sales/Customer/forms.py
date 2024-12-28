from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name_lo', 'VatNumber', 'Telphone', 'phone', 'Address', 'is_stop', 'balance']
        widgets = {
            'balance': forms.NumberInput(attrs={'step': '0.01'}),
        }

def clean_VatNumber(self):
        vat_number = self.cleaned_data.get('VatNumber')
        if Customer.objects.filter(VatNumber=vat_number).exists():
            raise forms.ValidationError("العميل الذي يحمل هذا الرقم الضريبي موجود بالفعل.")
        return vat_number