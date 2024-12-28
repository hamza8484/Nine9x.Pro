# CompanyInfo/urls.py
from django.urls import path
from . import views

app_name = 'Companyinfo'  # تأكد من إضافة app_name

urlpatterns = [
    path('add/', views.add_or_edit_company_info, name='add_company_info'),
    path('success/', views.company_info_success, name='company_info_success'),  # تأكد من أن هذا المسار موجود
]
