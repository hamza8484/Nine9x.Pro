# Generated by Django 5.1.3 on 2024-12-16 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='trial_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='trial_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
