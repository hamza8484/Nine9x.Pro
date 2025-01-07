# Generated by Django 5.1.3 on 2025-01-05 00:54

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
            name='ProgramSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('sidebar_color', models.CharField(default='#2980b9', max_length=7)),
                ('navbar_color', models.CharField(default='#34495e', max_length=7)),
                ('footer_color', models.CharField(default='#2c3e50', max_length=7)),
                ('text_color', models.CharField(default='#ffffff', max_length=7)),
                ('link_color', models.CharField(default='#1abc9c', max_length=7)),
                ('sidebar_font_size', models.IntegerField(default=14)),
                ('navbar_font_size', models.IntegerField(default=16)),
                ('footer_font_size', models.IntegerField(default=12)),
                ('body_font_size', models.IntegerField(default=14)),
                ('text_opacity', models.FloatField(default=1.0)),
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
