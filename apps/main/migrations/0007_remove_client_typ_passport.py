# Generated by Django 4.2.3 on 2023-09-15 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_holiday_options_sickleave_type_sick_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='typ_passport',
        ),
    ]
