from django import forms
from .models import CompanyInfo  

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo  
        fields = ['company_name', 'tax_number', 'email', 'commercial', 
                  'state', 'city', 'telephone_number', 'mobile_number', 
                  'note', 'address', 'logo']
        
widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
