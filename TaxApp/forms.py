from django import forms
from django.utils.translation import gettext_lazy as _  # استيراد _()

from .models import Tax

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['name', 'rate']  # تأكد من أن الحقول تتطابق مع نموذجك
        labels = {
            'name': _('اسم الضريبة'),  # إضافة الترجمة للاسم
            'rate': _('نسبة الضريبة'),  # إضافة الترجمة للنسبة
        }
        help_texts = {
            'name': _('أدخل اسم الضريبة هنا'),  # نص المساعدة للـ name
            'rate': _('أدخل نسبة الضريبة هنا (مثال: 5 أو 10)')  # نص المساعدة للـ rate
        }
def clean_rate(self):
    rate = self.cleaned_data.get('rate')
    if rate < 0 or rate > 100:
        raise forms.ValidationError(_('نسبة الضريبة يجب أن تكون بين 0 و 100.'))
    return rate
