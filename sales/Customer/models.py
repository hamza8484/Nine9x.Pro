from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name_lo = models.CharField(max_length=255)
    VatNumber = models.CharField(max_length=50)
    Telphone = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    Address = models.CharField(max_length=255)
    is_stop = models.BooleanField(default=False)
    
    # إضافة حقل الرصيد
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # إضافة حقل created مع auto_now_add=True
    created = models.DateTimeField(default=timezone.now)


    # إضافة المبلغ إلى الرصيد
    def add_balance(self, amount):
        # تأكد من أن amount هو من نوع Decimal
        self.balance += Decimal(amount)
        self.save()

    # خصم المبلغ من الرصيد
    def subtract_balance(self, amount):
        # تأكد من أن amount هو من نوع Decimal
        self.balance -= Decimal(amount)
        self.save()
        
     # تمثيل النصي للعميل
    def __str__(self):
        return self.name_lo    