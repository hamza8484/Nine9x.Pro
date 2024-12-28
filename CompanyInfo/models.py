from django.db import models
from django.utils.translation import gettext as _


class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=100, verbose_name=_("إسم الشركة"))
    tax_number = models.CharField(max_length=20, verbose_name=_("الرقم الضريبي"))
    email = models.EmailField(verbose_name=_("الإيميل"))
    commercial = models.CharField(max_length=20, verbose_name=_("السجل التجاري"))
    state = models.CharField(max_length=50, verbose_name=_("الدولة"))
    city = models.CharField(max_length=50, verbose_name=_("المدينة"))
    telephone_number = models.CharField(max_length=15, verbose_name=_("رقم الهاتف"))
    mobile_number = models.CharField(max_length=15, verbose_name=_("رقم الجوال"))
    note = models.TextField(verbose_name=_("ملاحظات"))
    address = models.TextField(verbose_name=_("العنوان"))
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name=_("الشعار"))
   

    def __str__(self):
        return self.company_name

