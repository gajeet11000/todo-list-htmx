from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms
from django.forms import widgets

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=widgets.TextInput())
    password = forms.CharField(widget=widgets.PasswordInput())