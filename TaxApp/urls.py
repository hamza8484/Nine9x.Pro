from django.urls import path
from . import views

app_name = 'taxapp'

urlpatterns = [
    path('add/', views.add_tax, name='add_tax'),
    path('list/', views.list_taxes, name='list_taxes'),
    #path('get_tax_rate/', views.get_tax_rate, name='get_tax_rate'),
    path('tax_rate/', views.tax_rate_view, name='tax_rate'),  # المسار الصحيح
]
