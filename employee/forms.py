from django import forms
from .models import SalaryPayment
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'mobile_number', 'phone_number', 'email', 'job_title', 'birth_date', 'id_card_number',
                  'marital_status', 'gender', 'nationality', 'hiring_date', 'department', 'base_salary', 'allowances',
                  'employment_status', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hiring_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class SalaryPaymentForm(forms.ModelForm):
    class Meta:
        model = SalaryPayment
        fields = ['employee', 'salary', 'allowances', 'payment_date', 'paid','accruals','deductions','accrual_date','deduction_date','accrual_reason','deduction_reason']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }    