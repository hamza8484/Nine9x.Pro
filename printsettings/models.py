from django.db import models


class PrinterSetting(models.Model):
    printer_name = models.CharField(max_length=255, unique=True)  # اسم الطابعة
    paper_size = models.CharField(max_length=10, choices=[('A4', 'A4'), ('8C', '8C')], default='A4')  # نوع الورق

    def __str__(self):
        return self.printer_name




class Printer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    is_connected = models.BooleanField(default=False)
    #category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='printers', null=True)

    def __str__(self):
        return f'{self.name or self.model} ({self.ip_address})'

class Category(models.Model):
    name_lo = models.CharField(max_length=100)
    name_fk = models.CharField(max_length=100)
    printer = models.CharField(max_length=100, blank=True, null=True)
    is_stop = models.BooleanField(default=False)

    def __str__(self):
        return self.name_lo
