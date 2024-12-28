from django import forms
from django.utils import timezone
from .models import PaymentVoucher, ReceiptVoucher
from purchases.models import Supplier
from sales.models import Customer
from django.core.exceptions import ValidationError

# نموذج سند الدفع
class PaymentVoucherForm(forms.ModelForm):
    class Meta:
        model = PaymentVoucher
        fields = ['supplier', 'amount', 'payment_method', 'voucher_number', 'date_created', 'description']

    # حقل المورد
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), empty_label="اختر المورد")

    # حقل المبلغ
    amount = forms.DecimalField(min_value=0, label="المبلغ")

    # حقل طريقة الدفع
    payment_method = forms.ChoiceField(choices=[('cash', 'نقداً'), ('Card', 'شبكة')])

    # حقل الوصف
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'أضف الوصف'}), required=False)

    # حقل رقم السند (عرض فقط - لا يمكن التعديل)
    voucher_number = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="رقم السند")

    # حقل تاريخ الإنشاء (عرض فقط - لا يمكن التعديل)
    date_created = forms.DateTimeField(initial=timezone.now, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="تاريخ الإنشاء")

    def save(self, commit=True):
        # إذا كانت الحقول فارغة، نقوم بتوليدها
        instance = super().save(commit=False)

        # تحقق من أن المبلغ المدفوع لا يتجاوز رصيد المورد
        if instance.supplier.balance < instance.amount:
            raise ValidationError("رصيد المورد غير كافٍ لتغطية المبلغ المدفوع.")

        # توليد رقم السند بناءً على الوقت الحالي
        if not instance.voucher_number:
            instance.voucher_number = f"VOUCHER-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        if not instance.date_created:
            instance.date_created = timezone.now()

        # خصم المبلغ من رصيد المورد بعد التحقق
        if commit:
            instance.save()
            instance.supplier.subtract_balance(instance.amount)

        return instance


# نموذج سند القبض
class ReceiptVoucherForm(forms.ModelForm):
    class Meta:
        model = ReceiptVoucher
        fields = ['customer', 'amount', 'payment_method', 'voucher_number', 'date_created', 'description']

    # حقل العميل
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), empty_label="اختر العميل")

    # حقل المبلغ
    amount = forms.DecimalField(min_value=0, label="المبلغ")

    # حقل طريقة الدفع
    payment_method = forms.ChoiceField(choices=[('cash', 'نقداً'), ('Card', 'شبكة')])

    # حقل الوصف
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'أضف الوصف'}), required=False)

    # حقل رقم السند (عرض فقط - لا يمكن التعديل)
    voucher_number = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="رقم السند")

    # حقل تاريخ الإنشاء (عرض فقط - لا يمكن التعديل)
    date_created = forms.DateTimeField(initial=timezone.now, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="تاريخ الإنشاء")

    def save(self, commit=True):
        # إذا كانت الحقول فارغة، نقوم بتوليدها
        instance = super().save(commit=False)

        # توليد رقم السند بناءً على الوقت الحالي
        if not instance.voucher_number:
            instance.voucher_number = f"RECEIPT-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        if not instance.date_created:
            instance.date_created = timezone.now()

        if commit:
            instance.save()

        return instance
