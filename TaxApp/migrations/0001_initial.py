# Generated by Django 5.1.3 on 2025-01-05 00:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='اسم الضريبة')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='نسبة الضريبة')),
            ],
            options={
                'verbose_name': 'الضريبة',
                'verbose_name_plural': 'الضرائب',
            },
        ),
    ]
