
from django.urls import path
from . import views

app_name = 'companyinfo'  # تأكد من إضافة app_name

urlpatterns = [
    path('add/', views.add_or_edit_company_info, name='add_company_info'),
    path('success/', views.company_info_success, name='company_info_success'),  # تأكد من أن هذا المسار موجود
    path('company-info/', views.get_company_info, name='get_company_info'),

]
