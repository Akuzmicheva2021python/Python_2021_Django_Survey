# Generated by Django 3.2 on 2021-10-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survay', '0016_auto_20211021_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresses',
            name='InsertDate',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='objectspersonals',
            name='InsertDate',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='sprdolgn',
            name='InsertDate',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='vobjects',
            name='InsertDate',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]
