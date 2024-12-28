from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_customer, name='add_customer'),
    path('customer-list/', views.customer_list, name='customer_list'),
    path('edit/<int:id>/', views.edit_customer, name='edit_customer'),  # تعديل عميل
    path('delete/<int:id>/', views.delete_customer, name='delete_customer'),  # حذف عميل
]

