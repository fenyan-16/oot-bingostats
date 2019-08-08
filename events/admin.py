from django.contrib import admin
from django.apps import apps
from .models import Event, Phase, Profile
admin.site.register(Profile)

admin.site.register(Event)
admin.site.register(apps.get_model('tournament', 'Tournament'))
admin.site.register(Phase)
admin.site.register(apps.get_model('tournament', 'Registration'))

admin.site.register(apps.get_model('tournament', 'Match1vs1'))
admin.site.register(apps.get_model('tournament', 'Bracket'))
admin.site.register(apps.get_model('tournament', 'Team'))
admin.site.register(apps.get_model('tournament', 'RegistrationTeam'))
admin.site.register(apps.get_model('tournament', 'League'))
admin.site.register(apps.get_model('tournament', 'TournamentsInLeague'))
admin.site.register(apps.get_model('tournament', 'Result'))