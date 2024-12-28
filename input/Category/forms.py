# forms.py
from django import forms
from .models import Category
from printsettings.models import Printer  # للوصول إلى الطابعات

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name_lo', 'name_fk', 'is_stop', 'printer']
    
    # إضافة حقل الطابعة مع جلب البيانات من قاعدة بيانات الطابعات
    printer = forms.ModelChoiceField(
        queryset=Printer.objects.all(),  # جلب جميع الطابعات من قاعدة البيانات
        required=True,                   # الحقل مطلوب
        label="اختر الطابعة",            # التسمية المعروضة للمستخدم
        empty_label="اختر طابعة"         # القيمة الافتراضية في القائمة المنسدلة
    )
