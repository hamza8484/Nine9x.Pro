# models.py
from django.db import models
from printsettings.models import Printer  # افترض أن لديك موديل للطابعات في printsettings

class Category(models.Model):
    name_lo = models.CharField(max_length=255, verbose_name="اسم القسم ع")
    name_fk = models.CharField(max_length=255, verbose_name="اسم القسم E")
    is_stop = models.BooleanField(default=False)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='categories', verbose_name="الطابعة")

    def __str__(self):
        return self.name_lo
