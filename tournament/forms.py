from django import forms

from .models import Tournament



class NewTournamentForm(forms.ModelForm):

    class Meta:
         model = Tournament
         fields = ('name', )

