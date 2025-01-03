# Generated by Django 5.1.3 on 2024-12-07 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lo', models.CharField(max_length=50, verbose_name='الاسم عربي')),
                ('name_fk', models.CharField(max_length=50, verbose_name='الاسم الاجنبي')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lo', models.CharField(max_length=50, verbose_name='الاسم عربي')),
                ('name_fk', models.CharField(max_length=50, verbose_name='الاسم الاجنبي')),
                ('is_stop', models.BooleanField(default=True, verbose_name='مغلق')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lo', models.CharField(max_length=50, verbose_name='الاسم عربي')),
                ('name_fk', models.CharField(max_length=50, verbose_name='الاسم الاجنبي')),
                ('codeUnit', models.CharField(max_length=50, verbose_name='رمز الوحدة')),
            ],
        ),
    ]
