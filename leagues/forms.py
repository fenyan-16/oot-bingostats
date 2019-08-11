from django import forms
from django.forms import ModelForm, DateField, ChoiceField
from django.forms.widgets import DateTimeBaseInput
from django.forms.formsets import BaseFormSet
from .models import TournamentsInLeague


class DateTimeInput(DateTimeBaseInput):
    format_key = 'DATETIME_INPUT_FORMATS'
    input_type = 'datetime-local'

class DateInput(forms.DateInput):
    input_type = 'date'

class NewLeagueForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    start_date = DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    registration_end_date = DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class LeagueForm(forms.ModelForm):
    class Meta:
        model = TournamentsInLeague
        fields = ('league',)
