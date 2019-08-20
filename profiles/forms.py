from django import forms
from django.forms import ModelForm, DateField, ChoiceField
from django.forms.widgets import DateTimeBaseInput
from django.forms.formsets import BaseFormSet
from .models import Userprofile



class EditProfileForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    start_date = DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    registration_end_date = DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))


