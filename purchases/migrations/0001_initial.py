# Generated by Django 5.1.3 on 2024-12-18 12:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configrate', '0002_programsettings'),
        ('input', '0003_alter_category_printer_alter_category_name_fk_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lo', models.CharField(max_length=255)),
                ('name_fk', models.CharField(max_length=255)),
                ('VatNumber', models.CharField(max_length=50)),
                ('TelPhone', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('Address', models.TextField()),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('is_stop', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInvoicelocal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ الإنشاء')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')),
                ('code', models.IntegerField(unique=True, verbose_name='number')),
                ('date', models.DateField(verbose_name='تاريخ الفاتورة')),
                ('is_stage', models.BooleanField(default=False, verbose_name='الحالة')),
                ('is_suspended', models.BooleanField(default=False, verbose_name='الحالة')),
                ('tax', models.FloatField(blank=True, null=True, verbose_name='الضريبة')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='التاريخ  ')),
                ('check_amount', models.FloatField(blank=True, null=True, verbose_name='المبغ')),
                ('supplier_bill_number', models.IntegerField(blank=True, null=True, verbose_name='رقم فاتورة المورد')),
                ('supplier_bill_date', models.DateField(blank=True, null=True, verbose_name='تاريخ فاتورة المورد')),
                ('stop', models.BooleanField(default=False, verbose_name='وقف')),
                ('amount', models.FloatField(blank=True, null=True, verbose_name='المجموع')),
                ('statement', models.CharField(max_length=100, verbose_name='ملاحظات')),
                ('reference_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='رقم المرجع')),
                ('total_amount', models.FloatField(verbose_name='مجموع الفاتورة')),
                ('discount', models.FloatField(default=0, verbose_name='الخصم')),
                ('discount_rate', models.FloatField(blank=True, null=True, verbose_name='نسبة الخصم %')),
                ('payment_method', models.CharField(choices=[('CASH', 'نقدي'), ('CARD', 'شبكة ')], default='CASH', max_length=10, verbose_name='طريقة الدفع')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_invoices', to='purchases.supplier', verbose_name='المورد')),
                ('supplir', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='purchases.supplier', verbose_name='المورد')),
            ],
            options={
                'verbose_name': 'مجموع ',
                'db_table': 'purchase_invoicelocal',
            },
        ),
        migrations.CreateModel(
            name='PurchaseInvoicelocalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ الإنشاء')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')),
                ('qty', models.PositiveIntegerField(verbose_name='الكمية')),
                ('free_qty', models.PositiveIntegerField(default=0, verbose_name='الكمية المتاحة')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='السعر')),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='تاريخ الانتهاء')),
                ('statement', models.CharField(blank=True, max_length=100, null=True, verbose_name='ملاحظات')),
                ('discount', models.FloatField(blank=True, default=0, null=True, verbose_name='الخصم')),
                ('discount_rate', models.FloatField(blank=True, null=True, verbose_name='نسبة الخصم %')),
                ('selling_price', models.FloatField(blank=True, null=True, verbose_name='سعر الشراء')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='input.items')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('purchase_invoicelocal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.purchaseinvoicelocal')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configrate.store')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configrate.unit')),
            ],
            options={
                'verbose_name': 'مجموع تفاصيل الفاتورة',
                'db_table': 'purchase_invoicelocal_details',
            },
        ),
    ]
