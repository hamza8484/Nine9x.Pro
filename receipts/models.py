from django.db import models
from django.contrib.auth.models import User
from sales.models import Customer  # إضافة استيراد نموذج العميل
from purchases.models import Supplier  # إضافة استيراد نموذج المورد
from datetime import date


class Receipt(models.Model):
    receipt_number = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_balance = models.DecimalField(max_digits=10, decimal_places=2)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'نقدي'), ('Card', 'بطاقة')])
    receipt_date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return f"Receipt {self.receipt_number} - {self.customer.name_lo}"

   


class Payment(models.Model):
    payment_number = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    #supplier_balance = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'نقدي'), ('Card', 'بطاقة')])
    payment_date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return f"Payment {self.payment_number} - {self.supplier.name_lo}"


