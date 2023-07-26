"""
Serializer for shopping list
"""

from rest_framework import serializers
from core.models import Store, Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'store']
        read_only_fields = ['id']


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'created', 'important']
        read_only_fields = ['id', 'created']
