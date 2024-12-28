# TaxApp/admin.py
from django.contrib import admin
from .models import Tax  # إضافة tax

admin.site.register(Tax)
