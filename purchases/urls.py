from django.urls import path
from .views import Supplier_view, SupplierJson
from . import views

urlpatterns = [
    # عرض الموردين
    path('suppliers_list/', views.supplier_list, name='suppliers_list'),  # عرض قائمة الموردين
    path('supplier/add/', views.add_supplier, name='add_supplier'),
    path('supplier/json/', views.SupplierJson.as_view(), name='SupplierJson'),  # تأكد من إضافة هذا المسار

    # صفحة عرض تفاصيل المورد
    path('supplier/<int:id>/', Supplier_view.as_view(), name='supplier_view'),  # عرض تفاصيل المورد
        
    # رابط التعديل: يجب أن يتطابق مع الرابط في الجافاسكربت
    path('supplier/edit/<int:id>/', Supplier_view.as_view(), name='edit_supplier'),
    
    # رابط الحذف: يجب أن يتطابق مع الرابط في الجافاسكربت
    path('supplier/delete/<int:id>/', Supplier_view.as_view(), name='delete_supplier'),

    # روابط فواتير المشتريات
    path('purchase/invoices/', views.purchase_invoices_list, name='purchase_invoices_list'),
    path('purchase/invoices/create/', views.create_purchase_invoice, name='create_purchase_invoice'),
    path('purchase/invoices/success/<str:invoice_code>/', views.purchase_invoice_success, name='purchase_invoice_success'),
]

