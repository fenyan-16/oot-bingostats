from django.contrib import admin
from django.apps import apps
from .models import Event, Phase, Profile
admin.site.register(Profile)

admin.site.register(Event)
admin.site.register(apps.get_model('tournament', 'Tournament'))
admin.site.register(Phase)
admin.site.register(apps.get_model('tournament', 'Registration'))

admin.site.register(apps.get_model('tournament', 'Match'))