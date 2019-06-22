from django.contrib import admin

from .models import Event, Tournament, Registration

admin.site.register(Event)
admin.site.register(Tournament)
admin.site.register(Registration)