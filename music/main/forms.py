from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
import re


class LoginForm(forms.Form):
    username = forms.CharField(label='Your Email/Username', max_length=100)
    password = forms.CharField(label='Your Password', max_length=100)


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Your Password', max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput, label='One more time?', max_length=100)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password1')
        password1 = self.cleaned_data.get('password2')
        if password != password1:
            raise ValidationError({'password1': ['The passwords did not match']})

        else:
            if password:
                if len(password) < 8:
                    raise ValidationError({'password1': ['Passwords must be of more than 8 characters']})

                pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
                if not bool(pattern.search(password)):
                    raise ValidationError(
                        {'password1': ['Password must contain alphabet characters, special characters and numbers']})

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError('User with this username already exists')
        else:
            return username
