from django import forms
from django.utils.translation import gettext_lazy as _  # استيراد الترجمة

class SupportEmailForm(forms.Form):
    name = forms.CharField(max_length=100, label=_('الاسم'))  # ترجمة التسمية
    email = forms.EmailField(label=_('البريد الإلكتروني'))  # ترجمة التسمية
    message = forms.CharField(widget=forms.Textarea, label=_('الرسالة'))  # ترجمة التسمية
