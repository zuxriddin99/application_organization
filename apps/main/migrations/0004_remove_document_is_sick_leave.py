# Generated by Django 4.2.3 on 2023-09-01 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_holiday_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='is_sick_leave',
        ),
    ]