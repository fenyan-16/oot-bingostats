# Generated by Django 2.2.2 on 2019-08-04 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0006_auto_20190804_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='bracket',
        ),
        migrations.CreateModel(
            name='RegistrationTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seed', models.IntegerField(null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Tournament')),
            ],
        ),
    ]
