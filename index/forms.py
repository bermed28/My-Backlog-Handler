from django import forms
from .models import Library_Model, Library_Membership
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LibraryAddForm(forms.ModelForm):

    class Meta:
        model = Library_Membership
        fields = ["is_finished",'last_played']
        widgets = {
            'last_played': forms.DateInput(format=('%m/%d/%Y'),
                                             attrs={'placeholder': 'mm/dd/yyyy',
                                                    'type': 'date'}),
        }
