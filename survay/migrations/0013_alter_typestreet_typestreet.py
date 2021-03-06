# Generated by Django 3.2 on 2021-10-21 18:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survay', '0012_auto_20211021_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typestreet',
            name='TypeStreet',
            field=models.CharField(blank=True, default='', help_text='Наименование типов: улица, переулок и т.п.', max_length=50, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-Я-_ ]+$', 'Разрешено использовать только буквы, пробел и дефис.', code='invalid_typestreet')], verbose_name='Наименование'),
        ),
    ]
