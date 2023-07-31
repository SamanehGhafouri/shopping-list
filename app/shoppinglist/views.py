from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import StoreForm, CustomUserCreationForm, ItemForm
from django.http import HttpResponse, HttpResponseRedirect
from .api_calls import APICalls as api


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

    if password1 != password2:
        "Tell user the password didn't match"
        return render(
            request,
            'shoppinglist/signupuser.html',
            {
                'form': CustomUserCreationForm,
                'error': 'Passwords did not match'
                }
            )
    user = authenticate(request,
                        email=username, password=password2)
    if user is not None:
        return render(
            request, 'shoppinglist/signupuser.html',
            {
                'form': CustomUserCreationForm,
                'error': 'This Username is already taken! Please login.'
                }
            )
    try:
        api.create_user(
            username, password2,
            first_name, last_name)
        user = authenticate(
            request,
            email=username,
            password=password2)
        if user is not None:
            login(request, user)
            token = api.create_token(email=username, password=password2)
            response = HttpResponse(token)
            response = redirect('createstore')
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
        token = api.create_token(
            request.POST['username'],
            request.POST['password'])
        response = HttpResponse("token from login-->", token)
        response = redirect('createstore')
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
        token = None
        response = HttpResponse(token)
        response = redirect('home')
        response.set_cookie('auth_token', token)
        return response


def createstore(request):
    token = request.COOKIES.get('auth_token')
    print("this is token from create store----->", token)
    if request.method == 'GET':
        if token:
            return render(
                request, 'shoppinglist/createstore.html',
                {'form': StoreForm()})
    important = request.POST.get("important")
    store_name = request.POST['store_name']
    if important == 'on':
        important_val = 'true'
    else:
        important_val = 'false'
    try:
        api.create_store(store_name, important_val, token)
        response = HttpResponse(token)
        response = redirect('currentstores')
        return response
    except ValueError:
        return render(
            request, 'shoppinglist/createstore.html',
            {'form': StoreForm(), 'error': 'Bad data!'})


def currentstores(request):
    token = request.COOKIES.get('auth_token')
    stores_data = api.get_stores(token)
    if request.method == 'GET':
        return render(
            request,
            'shoppinglist/currentstores.html',
            {'stores_data': stores_data})
    if "delete" in request.POST:
        if token:
            store_pk = int(request.POST['delete'])
            api.delete_store(store_pk, token)
            response = HttpResponse(token)
            response = HttpResponseRedirect(request.path_info)
            return response


def storeitemsview(request, pk):
    token = request.COOKIES.get('auth_token')
    store_pk = pk
    if token:
        if request.method == 'GET':
            items = api.get_items_of_a_store(store_pk, token)
            response = HttpResponse(token)
            response = render(
                request,
                'shoppinglist/storeitemsview.html',
                {'store_pk': store_pk,
                    'items': items, 'item_form': ItemForm()})
            return response
            # return render(request, 'shoppinglist/home.html')
        if "delete" in request.POST:
            if token:
                item_pk = int(request.POST['delete'])
                api.delete_store_item(store_pk, item_pk, token)
                response = HttpResponse(token)
                return HttpResponseRedirect(request.path_info)
        if "create" in request.POST:
            if token:
                item_name = request.POST['item_name']
                api.create_item(store_pk, item_name, token)
                items = api.get_items_of_a_store(store_pk, token)
                response = HttpResponse(token)
                return HttpResponseRedirect(request.path_info)


def editstore(request, pk):
    token = request.COOKIES.get('auth_token')
    if not token:
        return redirect('home')
    store = api.get_store_by_id(pk, token)
    store_pk = pk
    if request.method == 'GET':
        data = {'store_name': store['store_name']}
        return render(
            request,
            'shoppinglist/editstore.html',
            {'store-pk': pk, 'form': StoreForm(initial=data)}
            )
    store_name = request.POST['store_name']
    important = request.POST.get('important')
    if important == 'on':
        important_val = 'true'
    else:
        important_val = 'false'
    try:
        api.edit_store(store_pk, store_name, important_val, token)
        return redirect('currentstores')
    except ValueError:
        return render(
            request,
            'shoppinglist/editstore.html',
            {'store-pk': pk, 'form': StoreForm}
            )


def editstoreitem(request, storepk, itempk):
    token = request.COOKIES.get('auth_token')
    if not token:
        return redirect('home')
    item = api.get_item_by_store_id(storepk, itempk, token)
    data = {'item_name': item['name']}
    if request.method == 'GET':
        return render(
            request,
            'shoppinglist/editstoreitem.html',
            {'form': ItemForm(initial=data), 'storepk': storepk}
            )
    item_name = request.POST['item_name']
    api.edit_store_item(storepk, itempk, item_name, token)
    return redirect('storeitemsview', pk=storepk)
