from django import forms
from django.utils.translation import gettext_lazy as _  # استيراد الترجمة
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date','description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # تحديد نوع الحقل كـ "date"
        }
        # ترجمة الأسماء
        labels = {
            'name': _('إسم المصروف'),
            'amount': _('المبلغ'),
            'date': _('تاريخ المصروف'),
            'description': _('البيان'),
        }
