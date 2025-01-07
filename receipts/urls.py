from django.urls import path
from . import views

urlpatterns = [
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('payment_list/', views.payment_list, name='payment_list'),
    path('receipt_form/', views.receipt_form, name='receipt_form'),
    path('payment_form/', views.payment_form, name='payment_form'),
    path('get_supplier_balance/<int:supplier_id>/', views.get_supplier_balance, name='get_supplier_balance'),
     # عرض الرصيد المتبقي بعد الدفع بناءً على رقم الدفع
    path('payment/<int:payment_number>/balance/', views.get_balance_after_payment, name='payment_balance'),
    
    # عرض رصيد المورد بناءً على ID المورد
    path('supplier/<int:supplier_id>/balance/', views.get_supplier_balance, name='supplier_balance'),
]
