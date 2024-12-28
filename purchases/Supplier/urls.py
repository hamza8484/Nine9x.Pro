from django.urls import path
from .views import Supplier_view, SupplierJson
from . import views


urlpatterns = [
    path('list/', views.supplier_list, name='supplier_list'),
    # صفحة المورد
    path('supplier/', Supplier_view.as_view(), name='Supplier'),
    
    # رابط جلب البيانات بتنسيق JSON
    path('SupplierJson/', SupplierJson.as_view(), name='SupplierJson'),
    
    # رابط التعديل: يجب أن يتطابق مع الرابط في الجافاسكربت
    path('supplier/edit/<int:id>/', Supplier_view.as_view(), name='edit_supplier'),
    
    # رابط الحذف: يجب أن يتطابق مع الرابط في الجافاسكربت
    path('supplier/delete/<int:id>/', Supplier_view.as_view(), name='delete_supplier'),
    
    
]
