from django.contrib import admin

from .models import Event, Tournament

admin.site.register(Event)
admin.site.register(Tournament)