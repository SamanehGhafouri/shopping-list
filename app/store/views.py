"""
View for Store APIs
"""

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from core.models import Store, Item
from store import serializers
from django.shortcuts import get_object_or_404
from django.http import Http404


class StoreListView(generics.ListCreateAPIView):
    """Store list view"""
    serializer_class = serializers.StoreSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Get all stores created by user
    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)

    # Create stores
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Store detail view. GET/PUT/PATCH/DELETE stores by id"""
    serializer_class = serializers.StoreSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)


class ItemByStoreListView(generics.ListCreateAPIView):
    """Item by store list view"""
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Get all items for a store by store_id
    def get_queryset(self):
        store_id = self.kwargs['store_id']
        try:
            store = Store.objects.get(pk=store_id)
            if store:
                if store.user != self.request.user:
                    raise NotFound
                return Item.objects.filter(
                    store_id=store_id,
                    store__user=self.request.user
                    )
        except Store.DoesNotExist:
            raise Http404

    # Create items for a store by store_id
    def perform_create(self, serializer):
        store_id = self.kwargs['store_id']
        store = Store.objects.get(pk=store_id)
        if store.user == self.request.user:
            serializer.save(store=store)
        else:
            raise NotFound


class ItemByStoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Item by store detail view.
       GET/PUT/PATCH/DELETE by store_id and item_id
    """
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        store_id = self.kwargs['store_id']
        return Item.objects.filter(
            store_id=store_id,
            store__user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        item_id = self.kwargs['pk']
        obj = get_object_or_404(queryset, pk=item_id)
        self.check_object_permissions(self.request, obj)
        return obj
