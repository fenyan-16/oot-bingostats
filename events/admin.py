from django.contrib import admin
from django.apps import apps
from .models import Event, Phase

admin.site.register(Event)
admin.site.register(apps.get_model('tournament', 'Tournament'))
admin.site.register(Phase)
admin.site.register(apps.get_model('tournament', 'Registration'))

admin.site.register(apps.get_model('tournament', 'Match1vs1'))
admin.site.register(apps.get_model('tournament', 'Bracket'))
admin.site.register(apps.get_model('tournament', 'Team'))
admin.site.register(apps.get_model('tournament', 'RegistrationTeam'))
admin.site.register(apps.get_model('tournament', 'Standing'))
admin.site.register(apps.get_model('tournament', 'Result'))

admin.site.register(apps.get_model('leagues', 'League'))
admin.site.register(apps.get_model('leagues', 'TournamentsInLeague'))
admin.site.register(apps.get_model('leagues', 'Ratingpoints'))