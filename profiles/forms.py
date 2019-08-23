from django import forms
from django.forms import ModelForm, DateField, ChoiceField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
        attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Password confirmation'})

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

    def save(self, request):

        user = super(CreateUserForm, self).save(commit=False)
        user.is_active = False
        user.save()

        context = {
            # 'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
            'protocol': request.scheme,
            'username': self.cleaned_data.get('username'),
            'domain': request.META['HTTP_HOST'],
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }

        subject = render_to_string('djangobin/email/activation_subject.txt', context)
        email = render_to_string('djangobin/email/activation_email.txt', context)

        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user

class EditProfileForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    start_date = DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    registration_end_date = DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))


