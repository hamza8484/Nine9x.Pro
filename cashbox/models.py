from django.db import models
from django.utils import timezone

class Safe(models.Model):
    name = models.CharField(max_length=100, unique=True)  # اسم الخزنة
    creation_date = models.DateField(default=timezone.now)  # تاريخ انشاء الخزنة
    balance_added = models.DecimalField(max_digits=15, decimal_places=2)  # الرصيد المضاف للخزنة عند الإنشاء
    balance = models.DecimalField(max_digits=15, decimal_places=2, editable=False)  # الرصيد المتواجد (غير قابل للتعديل)
    notes = models.CharField(max_length=200,blank=True, null=True)  # الملاحظات

    def save(self, *args, **kwargs):
        # عند إضافة الخزنة، نقوم بتعيين الرصيد المتواجد إلى الرصيد المضاف
        if not self.balance:
            self.balance = self.balance_added
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    DEPOSIT = 'deposit'  # إيداع
    WITHDRAWAL = 'withdrawal'  # سحب
    
    TRANSACTION_TYPES = [
        (DEPOSIT, 'إيداع'),
        (WITHDRAWAL, 'سحب'),
    ]
    
    safe = models.ForeignKey(Safe, related_name='transactions', on_delete=models.CASCADE)  # الربط بالخزنة
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        default=DEPOSIT,
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # المبلغ
    date = models.DateTimeField(default=timezone.now)  # تاريخ المعاملة
    description = models.CharField(max_length=200,blank=True, null=True)  # وصف المعاملة

    def save(self, *args, **kwargs):
        # عند إضافة معاملة إيداع أو سحب، نقوم بتحديث الرصيد المتواجد في الخزنة
        if self.transaction_type == self.DEPOSIT:
            self.safe.balance += self.amount
        elif self.transaction_type == self.WITHDRAWAL:
            self.safe.balance -= self.amount
        
        # حفظ التحديثات في الخزنة
        self.safe.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date}"
