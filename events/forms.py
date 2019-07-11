from django import forms

from .models import Event, Phase, User, Profile

class NewEventForm(forms.ModelForm):

    class Meta:
         model = Event
         fields = ('name',)


class NewPhaseForm(forms.ModelForm):
    class Meta:
         model = Phase
         fields = ('name', 'mode',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location',)

