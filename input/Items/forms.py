from django import forms
from django.utils.translation import gettext as _
from input.models import Items

class ItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        # تحديث تهيئة الحقول في النموذج
        self.fields['name_lo'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['name_fk'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['items_type'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['unit'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['category'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['salse_price'].widget.attrs.update({
            'class': 'formset-field form-control'})
        self.fields['purch_price'].widget.attrs.update({
            'class': 'formset-field form-control'}) 
        self.fields['barcode'].widget.attrs.update({
            'class': 'formset-field form-control'})     
        self.fields['image'].widget.attrs.update({
            'class': 'formset-field form-control'})
        # إضافة حقل is_stop
        self.fields['is_stop'].widget.attrs.update({
            'class': 'formset-field form-control'})

    class Meta:
        model = Items
        fields = "__all__"  # سيشمل جميع الحقول بما فيها الحقول الجديدة
        labels = {
            'name_lo': _('الاسم المحلي'),
            'name_fk': _('الاسم الأجنبي'),
            'items_type': _('نوع العنصر'),
            'unit': _('الوحدة'),
            'category': _('الفئة'),
            'salse_price': _('سعر البيع'),
            'purch_price': _('سعر الشراء'),
            'barcode': _('الباركود'),
            'image': _('الصورة'),
            'is_stop': _('إيقاف العنصر'),
        }
