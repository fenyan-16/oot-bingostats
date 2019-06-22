from django import forms

from .models import Event, Tournament, Registration

class NewEventForm(forms.ModelForm):

    class Meta:
         model = Event
         fields = ('name',)

class NewTournamentForm(forms.ModelForm):

    class Meta:
         model = Tournament
         fields = ('name',)

class EventRegistrationForm(forms.ModelForm):

    class Meta:
         model = Registration
         fields = ()