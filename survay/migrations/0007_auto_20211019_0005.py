# Generated by Django 3.2 on 2021-10-18 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survay', '0006_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='ArhivDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата блокировки'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='PocketSize',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Размер пакета'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='VersionNumber',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='VersionNumber'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='VizitTime',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Время визитов'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='WEB',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='WEB'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='isNewObj',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='isNewObj'),
        ),
    ]
