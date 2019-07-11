from django import forms

from .models import Tournament, Registration



class NewTournamentForm(forms.ModelForm):

    class Meta:
         model = Tournament
         fields = ('name', )

class EventRegistrationForm(forms.ModelForm):

    class Meta:
         model = Registration
         fields = ()
