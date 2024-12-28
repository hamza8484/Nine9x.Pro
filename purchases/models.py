from django.db import models
from django.utils.translation import gettext_lazy as _
from CompanyInfo.models import CompanyInfo
from input.models import Items
from TaxApp.models import Tax
from django.contrib.auth.models import User
from configrate.models import Store
import uuid
from django.db import models, transaction
from datetime import date
from decimal import Decimal
from django.core.exceptions import ValidationError


# نموذج الفاتورة
class Invoice(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'نقدي'),
        ('network', 'شبكة')
    ]

    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    invoice_date = models.DateField(default=date.today)
    supplier = models.ForeignKey('purchases.Supplier', on_delete=models.CASCADE)
    supplier_invoice_number = models.CharField(max_length=50)
    supplier_invoice_date = models.DateField(default=date.today)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='cash'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_type = models.CharField(max_length=50, choices=[('price', 'خصم بالسعر'), ('percentage', 'خصم بالنسبة المئوية')])
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tax_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_invoice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    company_info = models.ForeignKey(CompanyInfo, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            print("Creating a new invoice number")
            invoice_counter = InvoiceCounter.objects.first()
            if not invoice_counter:
                print("No invoice counter found, creating one")
                invoice_counter = InvoiceCounter.objects.create(last_invoice_number=0)
            
            next_invoice_number = invoice_counter.last_invoice_number + 1
            invoice_counter.last_invoice_number = next_invoice_number
            invoice_counter.save()
            
            self.invoice_number = f"PUR-{str(next_invoice_number).zfill(4)}"
            print(f"New invoice number: {self.invoice_number}")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

    def calculate_total(self):
        # حساب إجمالي العناصر قبل الخصم
        total_purchase = sum(item.total for item in self.items.all())

        # تحويل total_purchase إلى Decimal إذا كان من نوع float
        total_purchase = Decimal(str(total_purchase))

        # حساب الخصم
        if self.discount_type == 'percentage':
            discount_amount = (Decimal(str(self.discount_value)) / Decimal('100')) * total_purchase
        else:  # الخصم بمبلغ ثابت
            discount_amount = Decimal(str(self.discount_value))

        # تطبيق الخصم على المجموع الكلي
        total_after_discount = total_purchase - discount_amount

        # حساب الضريبة
        self.total_tax = total_after_discount * (Decimal(str(self.tax_value)) / Decimal('100'))

        # حساب المجموع الكلي بعد الخصم والضريبة
        self.total_invoice = total_after_discount + self.total_tax
        self.total_purchase = total_purchase  # إضافة هذا لتخزين المجموع الأساسي في الكائن


# نموذج عنصر الفاتورة
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.item.name_lo} - {self.quantity} units"

    def calculate_total(self):
        # حساب إجمالي العنصر بناءً على الكمية والسعر والخصم
        self.total = Decimal(str(self.quantity)) * (Decimal(str(self.purchase_price)) - Decimal(str(self.discount)))
        self.save()  # حفظ التحديثات بعد الحساب


# نموذج المورد
class Supplier(models.Model):
    name_lo = models.CharField(max_length=255)
    name_fk = models.CharField(max_length=255)
    VatNumber = models.CharField(max_length=50)
    TelPhone = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    Address = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_stop = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_lo


# نموذج الرقم التسلسلي للفاتورة
class InvoiceCounter(models.Model):
    last_invoice_number = models.IntegerField(default=0)

    def __str__(self):
        return f"Last invoice number: {self.last_invoice_number}"


def save_invoice_and_items(invoice_data, items_data):
    try:
        # التحقق من وجود البيانات
        if not invoice_data or not items_data:
            raise ValidationError("Invoice data or items data is missing.")

        # استخدام المعاملات لضمان النزاهة
        with transaction.atomic():
            # إنشاء الفاتورة
            invoice = Invoice.objects.create(**invoice_data)
            print(f"Created invoice: {invoice}")

            # إضافة العناصر إلى الفاتورة
            for item_data in items_data:
                # التحقق من صحة البيانات قبل إضافة العنصر
                if not (item_data.get('quantity') and item_data['quantity'] > 0):
                    raise ValidationError(f"Invalid quantity for item {item_data}")
                if not (item_data.get('purchase_price') and item_data['purchase_price'] > 0):
                    raise ValidationError(f"Invalid purchase price for item {item_data}")
                if 'discount' not in item_data:
                    item_data['discount'] = 0.00  # إذا لم يكن هناك خصم

                # إضافة العنصر إلى الفاتورة
                item_data['invoice'] = invoice
                invoice_item = InvoiceItem.objects.create(**item_data)
                print(f"Created InvoiceItem: {invoice_item}")
                
                # حساب إجمالي العنصر بعد الحفظ
                invoice_item.calculate_total()

            # حساب الإجمالي للفاتورة بعد إضافة العناصر
            invoice.calculate_total()
            return invoice

    except ValidationError as e:
        print(f"Validation Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
