# expense/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),  # مسار إضافة المصاريف
    path('expenses/', views.expense_list, name='expense-list'),  # مسار عرض قائمة النفقات
    path('list/', views.expense_list, name='expense_list'),
    path('expense/edit/<int:expense_id>/', views.expense_edit, name='expense_edit'),  # رابط التعديل
]
