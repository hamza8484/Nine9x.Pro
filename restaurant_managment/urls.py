from django.contrib import admin
from django.urls import path, include ,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, ResetPasswordView, ChangePasswordView
# from CompanyInfo import views
from users.forms import LoginForm



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('configrate.urls')),
    path('', include('input.urls')),
    path('', include('purchases.urls')),
    path('api/', include('payments.urls')),
    path('', include('sales.urls')),
    path('', include('pos.urls')),
    path('api/', include('TaxApp.urls', namespace='taxapp')),
    path('support/', include('support.urls')),
    #path('employees/', include('employees.urls')),
    
    path('company/', include('CompanyInfo.urls', namespace='CompanyInfo')),  
    path('tax/', include('TaxApp.urls', namespace='TaxApp')), 
    path('expense/', include('expense.urls')),  # إضافة روابط المصروفات
    path('support/', include('support.urls')),
    path('check_server_connection/', views.check_server_connection, name='check_server_connection'),
    path('check-connection/', views.check_connection, name='check_connection'),
    path('change_language/', views.change_language, name='change_language'),
    path('printsettings/', include('printsettings.urls', namespace='printsettings')),  # تضمين namespace 
    
    
    path('', include('users.urls')),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login',template_name='users/login.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    


    path('oauth/', include('social_django.urls', namespace='social')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
