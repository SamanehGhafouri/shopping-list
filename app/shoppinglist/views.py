from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import StoreForm, CustomUserCreationForm, ItemForm
from django.http import HttpResponse, HttpResponseRedirect
from .api_calls import (
    create_token_api,
    create_user_api,
    create_store_api,
    get_stores_api,
    get_items_of_a_store_api,
    create_item_api,
    delete_store_item_api,
    delete_store_api,
    edit_store_api,
    edit_store_item_api)


def home(request):
    return render(request, 'shoppinglist/home.html')


def signupuser(request):

    if request.method == 'GET':
        return render(
            request, 'shoppinglist/signupuser.html',
            {'form': CustomUserCreationForm})
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']

    if password1 == password2:
        try:
            create_user_api(
                username, password2,
                first_name, last_name)
            user = authenticate(
                request,
                email=username,
                password=password2)
            if user is not None:
                login(request, user)
                token = create_token_api(email=username, password=password2)
                response = HttpResponse(
                    "token from signup user in cookie----->",
                    token)
                response = redirect('currentshopinglist')
                response.set_cookie('auth_token', token, max_age=86400)
                return response

        except IntegrityError:
            return render(
                request, 'shoppinglist/signupuser.html',
                {
                    'form': CustomUserCreationForm,
                    'error': 'The Username already exist'
                    }
                )
    "Tell user the password didn't match"
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
    user = authenticate(
        request,
        email=request.POST['username'],
        password=request.POST['password'])
    if user is not None and user.is_active:
        login(request, user)
        token = create_token_api(
            request.POST['username'],
            request.POST['password'])
        response = HttpResponse("token from login-->", token)
        response = redirect('create_store')
        response.set_cookie('auth_token', token, max_age=86400)
        return response
    return render(
        request,
        'shoppinglist/loginuser.html',
        {
            'form': AuthenticationForm(),
            'error': 'Username and password did not match'
            }
            )


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def create_store(request):
    token = request.COOKIES.get('auth_token')
    print("this is token from create store----->", token)
    if request.method == 'GET':
        if token:
            return render(
                request, 'shoppinglist/create_store.html',
                {'form': StoreForm()})
    important = request.POST.get("important")
    store_name = request.POST['store_name']
    if important == 'on':
        important_val = 'true'
    else:
        important_val = 'false'
    try:
        create_store_api(store_name, important_val, token)
        response = HttpResponse(token)
        response = redirect('currentshopinglist')
        return response
    except ValueError:
        return render(
            request, 'shoppinglist/create_store.html',
            {'form': StoreForm(), 'error': 'Bad data!'})


def currentshopinglist(request):
    token = request.COOKIES.get('auth_token')
    stores_data = get_stores_api(token)
    if request.method == 'GET':
        return render(
            request,
            'shoppinglist/currentshopinglist.html',
            {'stores_data': stores_data})
    if "delete" in request.POST:
        if token:
            store_pk = int(request.POST['delete'])
            delete_store_api(store_pk, token)
            response = HttpResponse(token)
            response = HttpResponseRedirect(request.path_info)
            return response


def storeitemsview(request, pk):
    token = request.COOKIES.get('auth_token')
    store_pk = pk
    if token:
        if request.method == 'GET':
            items = get_items_of_a_store_api(store_pk, token)
            response = HttpResponse(token)
            response = render(
                request,
                'shoppinglist/storeitemsview.html',
                {'store_pk': store_pk,
                    'items': items, 'item_form': ItemForm()})
            return response
            return render(request, 'shoppinglist/home.html')
        if "delete" in request.POST:
            if token:
                item_pk = int(request.POST['delete'])
                delete_store_item_api(store_pk, item_pk, token)
                response = HttpResponse(token)
                return HttpResponseRedirect(request.path_info)
        if "create" in request.POST:
            if token:
                item_name = request.POST['item_name']
                create_item_api(store_pk, item_name, token)
                items = get_items_of_a_store_api(store_pk, token)
                response = HttpResponse(token)
                return HttpResponseRedirect(request.path_info)


def editstore(request, pk):
    token = request.COOKIES.get('auth_token')
    if token:
        store_pk = pk
        if request.method == 'GET':
            return render(request,
                          'shoppinglist/editstore.html',
                          {'store-pk': pk, 'form': StoreForm})
        if request.method == 'POST':
            store_name = request.POST['store_name']
            important = request.POST.get('important')
            if important == 'on':
                important_val = 'true'
            else:
                important_val = 'false'
            try:
                edit_store_api(store_pk, store_name, important_val, token)
                return redirect('currentshopinglist')
            except ValueError:
                return render(request,
                              'shoppinglist/editstore.html',
                              {'store-pk': pk, 'form': StoreForm})


def edit_store_item(request, storepk, itempk):
    token = request.COOKIES.get('auth_token')
    if token:
        if request.method == 'GET':
            return render(request,
                          'shoppinglist/editstoreitem.html',
                          {'form': ItemForm()})
        item_name = request.POST['item_name']
        edit_store_item_api(storepk, itempk, item_name, token)
        return redirect('storeitemsview', pk=storepk)
