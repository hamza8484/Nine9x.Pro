from django.urls import path
from .views import SupplierView, supplier_list, SupplierJson, add_balance_view, subtract_balance_view, add_balance_form_view

urlpatterns = [
    path('supplier/add/', SupplierView.as_view(), name='Supplier'),  # إضافة مورد
    path('supplier/<int:id>/', SupplierView.as_view(), name='supplier_detail'),  # عرض وتعديل مورد
    path('supplier/<int:id>/delete/', SupplierView.as_view(), name='supplier_delete'),  # حذف مورد
    path('supplier/json/', SupplierJson.as_view(), name='supplier_json'),  # جلب الموردين بتنسيق JSON
    path('supplier/add_balance/<int:supplier_id>/<int:amount>/', add_balance_view, name='add_balance'),  # إضافة رصيد
    path('supplier/subtract_balance/<int:supplier_id>/<int:amount>/', subtract_balance_view, name='subtract_balance'),  # خصم رصيد
    path('supplier/add_balance_form/', add_balance_form_view, name='add_balance_form'),  # نموذج إضافة رصيد
]
