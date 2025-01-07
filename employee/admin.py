from django.contrib import admin
from .models import Employee

# تسجيل نموذج الموظف في لوحة الإدارة
admin.site.register(Employee)
