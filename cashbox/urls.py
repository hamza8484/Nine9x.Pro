# cashbox/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('safes/', views.safe_list, name='safe_list'),  # عرض الخزائن
    path('safes/add/', views.add_safe, name='add_safe'),  # إضافة خزنة جديدة
    path('transactions/', views.transaction_list, name='transaction_list'),  # عرض الحركات
    path('transactions/add/', views.add_transaction, name='add_transaction'),  # إضافة حركة مالية جديدة
]
