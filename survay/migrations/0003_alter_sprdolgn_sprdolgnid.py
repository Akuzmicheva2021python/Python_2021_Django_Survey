# Generated by Django 3.2 on 2021-10-17 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survay', '0002_sprdolgn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprdolgn',
            name='SprDolgnID',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='SprDolgnID'),
        ),
    ]
