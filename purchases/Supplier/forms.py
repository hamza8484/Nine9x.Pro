from django import forms
from purchases.models import Supplier
from django.utils.translation import gettext_lazy as _  # استيراد _() للترجمة

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        # تحديث الخصائص باستخدام الترجمة
        self.fields['name_lo'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['name_fk'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['VatNumber'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['TelPhone'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['phone'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['Address'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['is_stop'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['balance'].widget.attrs.update({
            'class': 'formset-field form-control'})
       
        
        # تطبيق الترجمة على أسماء الحقول (labels)
        self.fields['name_lo'].label = _('اسم المورد (باللغة المحلية)')
        self.fields['name_fk'].label = _('اسم المورد (باللغة الأجنبية)')
        self.fields['VatNumber'].label = _('رقم ضريبة القيمة المضافة')
        self.fields['TelPhone'].label = _('هاتف المورد')
        self.fields['phone'].label = _('الهاتف المحمول')
        self.fields['balance'].label = _(' الرصيد')
        self.fields['Address'].label = _('عنوان المورد')
        self.fields['is_stop'].label = _('هل المورد موقوف؟')

    class Meta:
        model = Supplier
        fields = "__all__"

class AddBalanceForm(forms.Form):
    supplier_id = forms.IntegerField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def add_balance(self):
        supplier_id = self.cleaned_data['supplier_id']
        amount = self.cleaned_data['amount']
        
        # التأكد من وجود المورد قبل إضافة الرصيد
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            supplier.balance += amount
            supplier.save()  # حفظ المورد مع التحديث الجديد
            return supplier
        except Supplier.DoesNotExist:
            raise forms.ValidationError(_('المورد غير موجود'))
