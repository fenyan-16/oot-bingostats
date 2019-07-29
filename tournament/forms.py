from django import forms

from .models import Tournament, Registration, Match1vs1



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
         model = Match1vs1
         fields = ('player1_result', 'player2_result', )