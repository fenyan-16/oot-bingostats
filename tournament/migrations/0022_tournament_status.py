# Generated by Django 2.2.2 on 2019-08-11 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0021_auto_20190811_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='status',
            field=models.IntegerField(default='1', null=True),
        ),
    ]
