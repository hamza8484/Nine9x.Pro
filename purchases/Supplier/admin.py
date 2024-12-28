# admin.py
from django.contrib import admin
from django.http import HttpResponse
from purchases.models import Supplier

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name_lo', 'name_fk', 'balance')

    def add_balance_action(self, request, queryset):
        for supplier in queryset:
            supplier.add_balance(1000)  # إضافة 1000 ريال إلى كل مورد محدد
            supplier.save()
        self.message_user(request, "تم إضافة 1000 ريال إلى الرصيد للموردين المحددين.")

    def subtract_balance_action(self, request, queryset):
        for supplier in queryset:
            supplier.subtract_balance(500)  # خصم 500 ريال من كل مورد محدد
            supplier.save()
        self.message_user(request, "تم خصم 500 ريال من الرصيد للموردين المحددين.")

    actions = [add_balance_action, subtract_balance_action]

admin.site.register(Supplier, SupplierAdmin)
