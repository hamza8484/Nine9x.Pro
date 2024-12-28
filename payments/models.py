from django.db import models
from decimal import Decimal
from django.utils import timezone
import uuid
from purchases.models import Supplier  # استيراد المورد لتجنب الاستيراد الدائري


# نموذج PaymentVoucher لدفع السند للمورد
class PaymentVoucher(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    voucher_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    PAYMENT_METHODS = [
        ('cash', 'نقداً'),
        ('Card', 'شبكة'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    def save(self, *args, **kwargs):
        # توليد رقم السند إذا لم يكن موجودًا
        if not self.voucher_number:
            # توليد رقم فريد باستخدام UUID ودمجه مع تاريخ الإنشاء
            self.voucher_number = f"PV{self.date_created.strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"

        # تحقق من أن رصيد المورد كافٍ لتغطية المبلغ
        if self.supplier.balance >= self.amount:
            # خصم المبلغ من رصيد المورد باستخدام طريقة subtract_balance
            self.supplier.subtract_balance(self.amount)
            super().save(*args, **kwargs)  # حفظ السند المالي
        else:
            raise ValueError("رصيد المورد غير كافٍ لتغطية المبلغ المدفوع.")

    def __str__(self):
        supplier_name = self.supplier.name_lo if self.supplier else 'Unknown'
        return f"Payment Voucher {self.voucher_number} - {supplier_name} - {self.amount} {self.date_created.strftime('%Y-%m-%d')}"


# نموذج ReceiptVoucher لاستلام السند من العميل
class ReceiptVoucher(models.Model):
    customer = models.ForeignKey('sales.Customer', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    voucher_number = models.CharField(max_length=100, unique=True, blank=True, null=True)

    PAYMENT_METHODS = [
        ('cash', 'نقداً'),
        ('Card', 'شبكة'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    def save(self, *args, **kwargs):
        # توليد رقم السند إذا لم يكن موجودًا
        if not self.voucher_number:
            # توليد رقم فريد باستخدام UUID ودمجه مع تاريخ الإنشاء
            self.voucher_number = f"RV{self.date_created.strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"

        super().save(*args, **kwargs)

    def __str__(self):
        # استيراد Customer هنا فقط عند الحاجة
        from sales.models import Customer
        customer_name = self.customer.name_lo if self.customer else 'Unknown'
        return f"Receipt Voucher {self.voucher_number} - {customer_name} - {self.amount} {self.date_created.strftime('%Y-%m-%d')}"


# نموذج PaymentMethod لتحديد طريقة الدفع
class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
