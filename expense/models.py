from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Expense(models.Model):
    # ترجمة verbose_name
    name = models.CharField(max_length=100,verbose_name=_('اسم المصروف'))  
    amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name=_('المبلغ'))
    date = models.DateField(default=timezone.now,verbose_name=_('تاريخ المصروف'))
    description = models.CharField(max_length=200,blank=True, null=True)
    def __str__(self):
        return self.name

