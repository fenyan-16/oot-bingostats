from django import forms

from .models import Tournament, Registration, Match



class NewTournamentForm(forms.ModelForm):

    class Meta:
         model = Tournament
         fields = ('name', )

class EventRegistrationForm(forms.ModelForm):

    class Meta:
         model = Registration
         fields = ()

class MatchResultForm(forms.ModelForm):

    class Meta:
         model = Match
         fields = ('player1_result', 'player2_result', )