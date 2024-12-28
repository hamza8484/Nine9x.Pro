# urls.py
from django.urls import path
from . import views  # تأكد من استيراد views هنا

urlpatterns = [
    path('Category/', views.category_view, name='category_view'),  # عرض الأقسام والطابعات
    #path('', views.category_view, name='category_view'),
]
