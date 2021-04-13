from django import forms
from .models import Library_Model, Library_Membership
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(max_length=120)
#
#     class Meta:
#         model = User
#         fields = ["email", "username", "password1", "password2"]
#
class LibraryAddForm(forms.ModelForm):
    last_played = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Library_Membership
        fields = ["is_finished"]
