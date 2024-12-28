# Generated by Django 5.1.3 on 2024-12-07 05:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configrate', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lo', models.CharField(max_length=100)),
                ('name_fk', models.CharField(max_length=100)),
                ('printer', models.CharField(blank=True, max_length=100, null=True)),
                ('is_stop', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ الإنشاء')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')),
                ('name_lo', models.CharField(max_length=50, unique=True, verbose_name='اسم الصنف عربي')),
                ('name_fk', models.CharField(default='', max_length=50, verbose_name='اسم الصنف إنجليزي')),
                ('barcode', models.CharField(max_length=50, unique=True, verbose_name='الباركود')),
                ('image', models.ImageField(default='default.jpg', upload_to='item', verbose_name='صورة الصنف')),
                ('purch_price', models.CharField(max_length=100, verbose_name='سعر الشراء')),
                ('salse_price', models.CharField(max_length=100, verbose_name='سعر البيع')),
                ('is_stop', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='input.category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('items_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configrate.items_type')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configrate.unit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purch_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salse_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_qty', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='input.items')),
            ],
        ),
        migrations.CreateModel(
            name='StoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ الإنشاء')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')),
                ('qty', models.IntegerField(verbose_name='الكمية')),
                ('selling_price', models.FloatField(verbose_name='سعر البيع')),
                ('purch_price', models.FloatField(verbose_name='سعر الشراء')),
                ('Items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='input.items')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('stor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configrate.store')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]