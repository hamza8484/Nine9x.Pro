# Generated by Django 5.1.3 on 2024-12-22 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0004_alter_invoice_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_invoice_number', models.IntegerField(default=0)),
            ],
        ),
    ]
