# printsettings/urls.py
from django.urls import path
from . import views

app_name = 'printsettings'

urlpatterns = [
  path('printer_settings/', views.printer_setting_view, name='printer_settings'),
 
  path('add_printer/', views.add_printer, name='add_printer'),
  path('search_printer/', views.search_printer, name='search_printer'),  # مسار البحث
  path('test_printer/', views.test_printer, name='test_printer'),
  path('update_printer/<int:pk>/', views.update_printer, name='update_printer'),
  path('delete_printer/<int:printer_id>/', views.delete_printer, name='delete_printer'),
  #path('printer_list/', views.printer_list, name='printer_list'),
]
