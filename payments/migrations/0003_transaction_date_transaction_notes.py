# Generated by Django 5.1.3 on 2024-12-18 16:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_receipt_customer_remove_receipt_supplier_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='transaction',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]