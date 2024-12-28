from django.urls import path, include  # تأكد من استيراد include هنا
from . import views

urlpatterns = [
  
    path('', include('purchases.Supplier.urls')), 
    path('create/', views.create_invoice, name='create_invoice'),
    path('invoice/list/', views.invoice_list, name='invoice_list'),
    path('invoice/print/<int:invoice_id>/', views.invoice_print, name='invoice_print'),
]

