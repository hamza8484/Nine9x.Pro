from django.db import models
from decimal import Decimal


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
    
    

    def add_balance(self, amount):
        """إضافة رصيد للمورد"""
        self.balance += amount
        self.save()

    def subtract_balance(self, amount):
        """خصم رصيد من المورد"""
        self.balance -= amount
        self.save()

   
