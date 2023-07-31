from django import forms
from django.forms import ModelForm, DateField, ChoiceField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail


class CreateUserForm(UserCreationForm):
    username = forms.CharField()
    username.widget = forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'aria-describedby': 'userHelp', 'placeholder': 'Enter username'})

    email = forms.CharField()
    email.widget = forms.TextInput(
        attrs={'type': 'email', 'class': 'form-control', 'aria-describedby': 'emailHelp', 'placeholder': 'Enter email'})

    password1 = forms.CharField()
    password1.label = "Password"
    password1.widget = forms.TextInput(
        attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})

    password2 = forms.CharField()
    password2.label = "Repeat password"
    password2.widget = forms.TextInput(
        attrs={'type': 'password', 'label_tag': 'Password repeat', 'class': 'form-control', 'placeholder': 'Password confirmation'})

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", )


    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("This field is required.")
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise ValidationError("Email is taken.")
        return self.cleaned_data['email']

class LoginForm(forms.Form):
    username = forms.CharField()
    username.widget = forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'aria-describedby': 'userHelp', 'placeholder': 'Enter username'})

    password = forms.CharField()
    password.widget = forms.TextInput(
        attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})


class EditProfileForm(forms.Form):

    twitch_username = forms.CharField()
    twitter_username = forms.CharField()

    class Meta:
        model = Userprofile
        fields = ("twitch_username", "twitter_username", "country")


    def set_userdata(self, userdata):
        if userdata.twitch_username:
            self.fields['twitch_username'].initial = userdata.twitch_username
        if userdata.twitter_username:
            self.fields['twitter_username'].initial = userdata.twitter_username
        if userdata.country:
            self.fields['country'].initial = userdata.country