from django.contrib import admin
from .models import Safe, Transaction

@admin.register(Safe)
class SafeAdmin(admin.ModelAdmin):
    list_display = ['name', 'creation_date', 'balance_added', 'balance', 'notes']
    search_fields = ['name']
    list_filter = ['creation_date']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['safe', 'transaction_type', 'amount', 'date', 'description']
    search_fields = ['safe__name', 'description']
    list_filter = ['transaction_type', 'date']
