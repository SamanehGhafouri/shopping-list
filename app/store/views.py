"""
View for Store APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Store
from store import serializers


class StoreViewSet(viewsets.ModelViewSet):
    """API endpoint that allows store in
    shopping list to be viewed or edited"""
    queryset = Store.objects.all().order_by('-created')
    serializer_class = serializers.StoreSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve stores for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.StoreSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new store"""
        serializer.save(user=self.request.user)
