# Generated by Django 5.1.3 on 2024-12-22 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0006_alter_invoice_invoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='supplier_invoice_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
