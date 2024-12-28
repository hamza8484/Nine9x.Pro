# Generated by Django 5.1.3 on 2024-12-19 20:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CompanyInfo', '0001_initial'),
        ('input', '0003_alter_category_printer_alter_category_name_fk_and_more'),
        ('payments', '0005_paymentmethod'),
        ('purchases', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseinvoicelocaldetails',
            name='purchase_invoicelocal',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoicelocaldetails',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoicelocaldetails',
            name='item',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoicelocaldetails',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoicelocaldetails',
            name='store',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoicelocaldetails',
            name='unit',
        ),
        migrations.AlterField(
            model_name='supplier',
            name='Address',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('invoice_date', models.DateField()),
                ('supplier_invoice_number', models.CharField(max_length=50)),
                ('supplier_invoice_date', models.DateField()),
                ('warehouse', models.CharField(max_length=100)),
                ('total_purchase', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('discount_type', models.CharField(choices=[('price', 'خصم بالسعر'), ('percentage', 'خصم بالنسبة المئوية')], max_length=50)),
                ('discount_value', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('tax_value', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('total_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_invoice', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('company_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CompanyInfo.companyinfo')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentmethod')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.supplier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='purchases.invoice')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='input.items')),
            ],
        ),
        migrations.DeleteModel(
            name='PurchaseInvoicelocal',
        ),
        migrations.DeleteModel(
            name='PurchaseInvoicelocalDetails',
        ),
    ]