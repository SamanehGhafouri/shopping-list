from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django import forms
import requests


def home(request):
    return render(request, 'shoppinglist/home.html')


class CustomUserCreationForm(UserCreationForm):

    first_name = forms.CharField(
        label='First Name',
        min_length=5, max_length=150)
    last_name = forms.CharField(
        label='Last Name', min_length=5,
        max_length=150)


def signupuser(request):

    if request.method == 'GET':
        return render(
            request, 'shoppinglist/signupuser.html',
            {'form': CustomUserCreationForm})
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if password1 == password2:
            body = {
                'email': username,
                'password': password2,
                'first_name': first_name,
                'last_name': last_name
            }
            try:
                requests.post(
                    'http://127.0.0.1:8000/api/user/create/',
                    headers={'Content-Type': 'application/json'},
                    json=body)

                user = authenticate(
                    request,
                    email=username,
                    password=password2)

                if user is not None:
                    login(request, user)
                    return redirect('currentshopinglist')
            except IntegrityError:
                return render(
                    request, 'shoppinglist/signupuser.html',
                    {
                        'form': CustomUserCreationForm,
                        'error': 'The Username already exist'
                        }
                    )

        else:
            "Tell user the password didn't match"
            print("hello")
            return render(
                request,
                'shoppinglist/signupuser.html',
                {
                    'form': CustomUserCreationForm,
                    'error': 'Passwords did not match'
                    }
                )


def loginuser(request):
    if request.method == 'GET':
        return render(
            request, 'shoppinglist/loginuser.html',
            {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request,
            email=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(
                request, 'shoppinglist/loginuser.html',
                {
                    'form': AuthenticationForm(),
                    'error': 'Username and password did not match'
                    }
                )
        else:
            login(request, user)
            return redirect('currentshopinglist')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currentshopinglist(request):
    return render(
        request,
        'shoppinglist/currentshopinglist.html')
