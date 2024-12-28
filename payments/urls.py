from django.urls import path
from . import views

urlpatterns = [
    # إضافة سند الدفع
    path('add_payment_voucher/', views.add_payment_voucher, name='add_payment_voucher'),
    path('voucher_list/', views.voucher_list, name='voucher_list'),
    path('voucher/<int:id>/', views.voucher_detail, name='voucher_detail'),
    path('supplier_voucher/<str:voucher_number>/', views.supplier_voucher_detail, name='supplier_voucher_detail'),

    # إضافة سند القبض
    path('add_receipt_voucher/', views.add_receipt_voucher, name='add_receipt_voucher'),
    
    # عرض تفاصيل سند الدفع
    path('payment_voucher/<str:voucher_number>/', views.payment_voucher_detail, name='payment_voucher_detail'),
    
    # عرض تفاصيل سند القبض
    path('receipt_voucher/<str:voucher_number>/', views.receipt_voucher_detail, name='receipt_voucher_detail'),
    
    # عرض جميع سندات الدفع
    path('payment_vouchers/', views.payment_voucher_list, name='payment_voucher_list'),

    # عرض جميع سندات القبض
    path('receipt_vouchers/', views.receipt_voucher_list, name='receipt_voucher_list'),
]
