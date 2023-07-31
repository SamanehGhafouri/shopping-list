"""
Front end urls
"""
from django.urls import path
from shoppinglist import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('createstore/', views.createstore, name='createstore'),
    path(
        'currentstores/',
        views.currentstores,
        name='currentstores'),
    path(
        'currentstores/<int:pk>/items/',
        views.storeitemsview,
        name='storeitemsview'),
    path(
        'editstore/<int:pk>/',
        views.editstore,
        name='editstore'
    ),
    path(
        'editstoreitem/<int:storepk>/<int:itempk>/',
        views.editstoreitem,
        name='editstoreitem'
    ),
]
