from django.urls import path
from . import views
from .views import get_salary_and_allowances

urlpatterns = [
    path('', views.employee_list, name='employee_list'),  # لعرض قائمة الموظفين
    path('add/', views.add_employee, name='add_employee'),  # لإضافة موظف جديد
    path('edit/<int:id>/', views.edit_employee, name='edit_employee'),  # لتعديل موظف
    path('details/<int:id>/', views.employee_detail, name='employee_detail'),  # لعرض تفاصيل الموظف
    path('employees/details/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('salary/create/', views.create_salary_payment, name='create_salary_payment'),
    path('salary-payment-list/', views.salary_payment_list, name='salary_payment_list'),
    path('get_salary_and_allowances/<int:employee_id>/', get_salary_and_allowances, name='get_salary_and_allowances'),
    path('salary-payments/', views.salary_list, name='salary_payment_list'),
    path('salary-payment/print/<int:payment_id>/', views.print_salary_details, name='print_salary_details'),

]
