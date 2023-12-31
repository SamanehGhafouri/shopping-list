"""
Customized forms for front end
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm


class ItemForm(forms.Form):

    item_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True})
        )


class StoreForm(forms.Form):

    store_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True})
        )
    important = forms.BooleanField(required=False)


class CustomUserCreationForm(UserCreationForm):

    first_name = forms.CharField(
        label='First Name',
        min_length=1, max_length=150)
    last_name = forms.CharField(
        label='Last Name', min_length=1,
        max_length=150)
