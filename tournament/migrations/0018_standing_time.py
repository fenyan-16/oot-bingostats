# Generated by Django 2.2.2 on 2019-08-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0017_auto_20190811_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='standing',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]