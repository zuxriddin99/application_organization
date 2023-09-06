# Generated by Django 4.2.3 on 2023-09-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_document_is_sick_leave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='type_holiday',
            field=models.CharField(blank=True, choices=[('Отпуск без содержания', 'Отпуск без содержания'), ('Отпуск по уходу за ребенком', 'Отпуск по уходу за ребенком'), ('Ежегодный отпуск', 'Ежегодный отпуск')], null=True, verbose_name='Тип отпуск'),
        ),
    ]