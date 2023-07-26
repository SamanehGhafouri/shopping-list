"""
Store app URL mapping
"""

from django.urls import path
from store import views

urlpatterns = [
    path(
        'stores/',
        views.StoreListView.as_view(),
        name='store-list-view'),
    path(
        '<int:pk>/',
        views.StoreDetailView.as_view(),
        name='store-detail-view'),
    path(
        '<int:store_id>/items/',
        views.ItemByStoreListView.as_view(),
        name='item-list-by-store'),
    path(
        '<int:store_id>/item/<int:pk>/',
        views.ItemByStoreDetailView.as_view(),
        name='item-detail-by-store'),
]
