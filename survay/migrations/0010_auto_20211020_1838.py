# Generated by Django 3.2 on 2021-10-20 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survay', '0009_objects'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objects',
            options={'verbose_name': 'Объекты', 'verbose_name_plural': 'Объекты'},
        ),
        migrations.AlterModelTable(
            name='objects',
            table='Objects',
        ),
    ]