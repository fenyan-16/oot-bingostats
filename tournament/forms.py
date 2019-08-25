from django import forms
from django.forms import ModelForm, DateField, ChoiceField
from django.forms.widgets import DateTimeBaseInput
from django.forms.formsets import BaseFormSet
from .models import Tournament, Registration, Match1vs1, Bracket, Standing
from leagues.models import TournamentsInLeague


class DateTimeInput(DateTimeBaseInput):
    format_key = 'DATETIME_INPUT_FORMATS'
    input_type = 'datetime-local'

class DateInput(forms.DateInput):
    input_type = 'date'

class NewTournamentForm(forms.Form):

    FORMAT_CHOICES = [
        ('1', '1vs1'),
        ('2', '2vs2'),
        ('3', '3vs3'),
        ('4', '4vs4'),
        ('5', '5vs5'),
    ]

    CHOICES = [('1', 'Player create Teams'),
               ('2', 'Teams by seeding'),
               ('3', 'Teams by admin')]

    name = forms.CharField()
    description = forms.CharField()
    date = DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # team_format = forms.ChoiceField(choices=FORMAT_CHOICES)
    # team_creation_mode = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class NewBracketForm(forms.ModelForm):

    class Meta:
         model = Bracket
         fields = ('mode',)

class EventRegistrationForm(forms.ModelForm):

    class Meta:
         model = Registration
         fields = ()

class LeagueForm(forms.ModelForm):
    class Meta:
        model = TournamentsInLeague
        fields = ('league',)


class ReportStandingsForm(forms.ModelForm):
    class Meta:
        model = Standing
        fields = ('user', 'result',)

