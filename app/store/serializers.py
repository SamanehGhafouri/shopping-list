"""
Serializer for shopping list
"""

from rest_framework import serializers

from core.models import Store


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'created', 'important']
        read_only_fields = ['id', 'created']
