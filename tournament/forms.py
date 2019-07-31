from django import forms

from .models import Tournament, Registration, Match1vs1, Bracket



class NewTournamentForm(forms.ModelForm):

    class Meta:
         model = Tournament
         fields = ('name', 'description', 'max_participants',)

class NewBracketForm(forms.ModelForm):

    class Meta:
         model = Bracket
         fields = ('mode',)

class EventRegistrationForm(forms.ModelForm):

    class Meta:
         model = Registration
         fields = ()

class MatchResultForm(forms.ModelForm):

    class Meta:
         model = Match1vs1
         fields = ('player1_result', 'player2_result', )