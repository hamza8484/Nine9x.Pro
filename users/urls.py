from django.urls import path
from .views import home, profile, RegisterView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='index'),
    path('profile/', profile, name='users-profile'),
    path('home/', views.home, name='users-home'), 
    path('register/', views.UserRegisterView.as_view(), name='register'),  # تأكد من وجود هذا السطر
    path('users-register/', views.UserRegisterView.as_view(), name='users-register'),  # تأكد من وجود هذا السطر
    path('settings/', views.settings_view, name='settings'),
    path('change_language/', views.change_language, name='change_language'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # صفحة الرئيسة
    
]
