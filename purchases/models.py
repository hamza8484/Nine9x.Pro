import traceback
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from purchases.Supplier.models import Supplier
from configrate.models import Store, Unit
from input.models import Items
from TaxApp.models import Tax

from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from django.db.models import F, Sum, FloatField, Q

class PurchaseInvoice(models.Model):
    invoice_code = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_invoice_number = models.CharField(max_length=50)
    supplier_invoice_date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'نقدي'), ('card', 'شبكة')])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    discount_type = models.CharField(max_length=20, choices=[('amount', 'خصم بالسعر'), ('percentage', 'خصم بالنسبة المئوية')], null=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tax_value = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_code:
            self.invoice_code = f"PUR-{str(self.id).zfill(4)}"
        
        # حساب الإجمالي بناءً على التفاصيل
        if not self.total_value:
            self.total_value = sum(detail.total for detail in self.details.all())
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_code

    class Meta:
        db_table = "purchase_invoice"
        verbose_name = _("فاتورة مشتريات")  # ترجمة النص

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, related_name='details', on_delete=models.CASCADE)
    Items = models.ForeignKey(Items, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = (self.quantity * self.price) - (self.discount or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Items.name} - {self.quantity} x {self.price}"

    class Meta:
        db_table = "invoice_detail"
        verbose_name = _("تفاصيل الفاتورة")  # ترجمة النص

class PurchaseInvoicelocal(PurchaseInvoice):
    class Meta:
        db_table = "purchase_invoicelocal"
        verbose_name = _("فاتورة مشتريات محلية")

    def __str__(self):
        return f"{self.invoice_code} - {self.get_payment_method_display()}"
