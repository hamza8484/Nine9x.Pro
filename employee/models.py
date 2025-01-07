from django.db import models
from datetime import date


class Employee(models.Model):
    # رقم الموظف يتم توليده تلقائيًا وليس كحقل AutoField
    employee_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    # باقي الحقول كما هي
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    mobile_number = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    job_title = models.CharField(max_length=50)
    birth_date = models.DateField()
    id_card_number = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=20, choices=[('single', 'أعزب'), ('married', 'متزوج')])
    gender = models.CharField(max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')])
    nationality = models.CharField(max_length=50)
    hiring_date = models.DateField()
    department = models.CharField(max_length=50)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    employment_status = models.CharField(max_length=20, choices=[
        ('active', 'على رأس العمل'), 
        ('inactive', 'موقف عن العمل')
        ])
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # إذا لم يكن هناك رقم موظف (في حالة الموظف الأول أو إذا لم يتم تعيين الرقم بعد)
        if not self.employee_number:
            # نحصل على آخر رقم موظف، ونقوم بزيادة الرقم بـ 1
            last_employee = Employee.objects.all().order_by('-id').first()
            if last_employee:
                last_employee_number = last_employee.employee_number
                last_number = int(last_employee_number.split('-')[1])  # نفصل الجزء الرقمي
                self.employee_number = f"EMP-{last_number + 1}"  # زيادة الرقم بمقدار 1
            else:
                self.employee_number = "EMP-1001"  # إذا كانت أول مرة، نبدأ بـ EMP-1001
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



from django.core.exceptions import ValidationError

class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # الراتب الأساسي
    allowances = models.DecimalField(max_digits=10, decimal_places=2)  # البدلات
    accruals = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # الاستحقاق
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # الاستقطاع
    accrual_date = models.DateField(default=date.today)  # تاريخ الاستحقاق
    deduction_date = models.DateField(default=date.today)  # تاريخ الاستقطاع
    accrual_reason = models.CharField(max_length=255, blank=True, null=True)  # سبب الاستحقاق
    deduction_reason = models.CharField(max_length=255, blank=True, null=True)  # سبب الاستقطاع
    payment_date = models.DateField(default=date.today)  # تاريخ الدفع
    paid = models.BooleanField(default=False)  # حالة الدفع (هل تم الدفع أم لا)

    def total_salary(self):
        # حساب الراتب الإجمالي (الراتب الأساسي + البدلات + الاستحقاق - الاستقطاع)
        return self.salary + self.allowances + self.accruals - self.deductions

    def clean(self):
        # تحقق من أنه لا يتم دفع الراتب لنفس الموظف في نفس الشهر
        existing_payment = SalaryPayment.objects.filter(
            employee=self.employee,
            payment_date__year=self.payment_date.year,
            payment_date__month=self.payment_date.month
        ).exists()
        
        if existing_payment:
            raise ValidationError(f"تم دفع راتب الموظف في شهر {self.payment_date.strftime('%B %Y')}.")
    
    def __str__(self):
        return f"{self.employee.name} - {self.payment_date}"

