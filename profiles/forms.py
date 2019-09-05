from django import forms
from django.forms import ModelForm, DateField, ChoiceField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile
from django_countries.fields import CountryField
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
    password1.widget = forms.TextInput(
        attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})

    password2 = forms.CharField()
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
    country = CountryField().formfield()

    class Meta:
        model = Userprofile
        fields = ("twitch_username", "country")


    def set_userdata(self, userdata):
        self.fields['twitch_username'].initial = userdata.twitch_username
        self.fields['country'].initial = userdata.country