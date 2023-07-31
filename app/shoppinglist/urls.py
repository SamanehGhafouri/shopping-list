"""
Front end urls
"""
from django.urls import path
from shoppinglist import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_user, name='signup-user'),
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('create-store/', views.create_store, name='create-store'),
    path(
        'current-stores/',
        views.current_stores,
        name='current-stores'),
    path(
        'current-stores/store/<int:pk>/items/',
        views.store_items,
        name='store-items'),
    path(
        'current-stores/store/<int:pk>/',
        views.edit_store,
        name='edit-store'
    ),
    path(
        'current-stores/store/<int:storepk>/item/<int:itempk>/',
        views.edit_store_item,
        name='edit-store-item'
    ),
]
