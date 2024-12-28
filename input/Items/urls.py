
from . import views


from .views import inventory_list
from .views import get_item_details
from .views import get_items_list
from django.urls import path, include


urlpatterns = [
    path('Items/', views.Items_item.as_view(), name='Items'),
    path('ItemsJson/', views.ItemsJson.as_view(), name='ItemsJson'),
    path('inventory/', inventory_list, name='inventory_list'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('api/items/', views.get_items, name='get_items'),
    path('get_items_list/', views.get_items_list, name='get_items_list'),
    path('get_item_details/', get_item_details, name='get_item_details'),
    path('get_item_by_barcode/', views.get_item_by_barcode, name='get_item_by_barcode'),
]
