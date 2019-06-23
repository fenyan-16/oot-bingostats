from django.contrib import admin

from .models import Event, Tournament, Registration, Phase

admin.site.register(Event)
admin.site.register(Tournament)
admin.site.register(Phase)
admin.site.register(Registration)