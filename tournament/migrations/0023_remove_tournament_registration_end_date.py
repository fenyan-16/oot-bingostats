# Generated by Django 2.2.2 on 2019-08-25 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0022_tournament_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='registration_end_date',
        ),
    ]
