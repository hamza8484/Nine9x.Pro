from django.db import models
from parent.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import transaction, IntegrityError
import datetime
from django.core.exceptions import ObjectDoesNotExist, FieldError, MultipleObjectsReturned
from django.db.models import F, Sum, FloatField, Q
from django.utils.translation import gettext_lazy as _  # تم استيراد gettext_lazy
from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from configrate.models import Unit, Store
from input.models import Items
from parent.models import BaseModel
import traceback
from sales.Customer.models import Customer


class SalesOperation(BaseModel):
    code = models.CharField(max_length=50)
    date = models.DateField(verbose_name=_("التاريخ"))  # ترجمة النص
    is_stage = models.BooleanField(verbose_name=_("هل هو مرحلة؟"), default=False)  # ترجمة النص
    is_suspended = models.BooleanField(verbose_name=_("هل هو موقوف؟"), default=False)  # ترجمة النص
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        verbose_name=_("العميل"),  # ترجمة النص
    )
    tax = models.FloatField(verbose_name=_("الضريبة"), blank=True, null=True)  # ترجمة النص
    due_date = models.DateField(verbose_name=_("تاريخ الاستحقاق"), null=True, blank=True)  # ترجمة النص
    check_amount = models.FloatField(_("قيمة الشيك"), null=True, blank=True)  # ترجمة النص
    stop = models.BooleanField(_("إيقاف"), default=False)  # ترجمة النص
    amount = models.FloatField(_("إجمالي الفاتورة المحلية"), null=True, blank=True)  # ترجمة النص
    statement = models.CharField(verbose_name=_("بيان"), max_length=100)  # ترجمة النص
    reference_number = models.CharField(
        verbose_name=_("رقم المرجع"), max_length=100, null=True, blank=True  # ترجمة النص
    )
    total_amount = models.FloatField(_("إجمالي المبلغ"))  # ترجمة النص
    discount = models.FloatField(_("الخصم"), default=0)  # ترجمة النص
    discount_rate = models.FloatField(_("معدل الخصم %"), null=True, blank=True)  # ترجمة النص
    
    def __str__(self):
        return str(self.code)

    class Meta:
        abstract = True


class SalesOperationDetails(BaseModel):
    item = models.ForeignKey(Items, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(verbose_name=_("الكمية"))  # ترجمة النص
    free_qty = models.PositiveIntegerField(verbose_name=_("الكمية المجانية"), default=0)  # ترجمة النص
    statement = models.CharField(
        verbose_name=_("بيان"), max_length=100, null=True, blank=True  # ترجمة النص
    )
    discount = models.FloatField(_("الخصم"), null=True, blank=True, default=0)  # ترجمة النص
    discount_rate = models.FloatField(_("معدل الخصم %"), null=True, blank=True)  # ترجمة النص
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, null=True, blank=True
    )
    
    def __str__(self):
        return str(self.item)

    class Meta:
        abstract = True


class SalesInvoicelocal(SalesOperation):
    PAYMENT_METHOD_CHOICES = [
        ('cash', _('نقدي')),
        ('credit_card', _('شبكة ')),
        
    ]
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        verbose_name=_("طريقة الدفع")  # ترجمة النص
    )

    class Meta:
        db_table = "Sales_invoicelocal"
        verbose_name = _("فاتورة مبيعات محلية")  # ترجمة النص

    def __str__(self):
        return f"{self.code} - {self.get_payment_method_display()}"


class SalesInvoicelocalDetails(SalesOperationDetails):
  
    selling_price = models.FloatField(_("سعر البيع"), null=True, blank=True)  # ترجمة النص
    Sales_invoicelocal = models.ForeignKey(
        SalesInvoicelocal, on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = "Sales_invoicelocal_details"
        verbose_name = _("تفاصيل فاتورة مبيعات محلية")  # ترجمة النص

class PaymentTransaction(BaseModel):
    TRANSACTION_TYPES = [
        ('credit', _('دائن')),  # العميل دفع المال
        ('debit', _('مدين')),   # العميل عليه دفع المال
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("العميل"))
    amount = models.FloatField(_("المبلغ"))
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='debit')
    transaction_date = models.DateField(_("تاريخ المعاملة"), default=datetime.date.today)
    statement = models.CharField(_("البيان"), max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.customer.name_lo} - {self.amount} - {self.get_transaction_type_display()}"
