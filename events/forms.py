from django import forms

from .models import Event, Tournament, Registration, Phase

class NewEventForm(forms.ModelForm):

    class Meta:
         model = Event
         fields = ('name',)

class NewTournamentForm(forms.ModelForm):

    class Meta:
         model = Tournament
         fields = ('name', 'max_participants', )

class NewPhaseForm(forms.ModelForm):
    class Meta:
         model = Phase
         fields = ('name', 'mode',)

class EventRegistrationForm(forms.ModelForm):

    class Meta:
         model = Registration
         fields = ()