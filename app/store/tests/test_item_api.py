"""
Tests for Items APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Item, Store

from store.serializers import ItemSerializer


def item_url(store_id):
    """Create and return an item URL"""
    return reverse('item-list-by-store', args=[store_id])


def item_detail_url(store_id, pk):
    """Create and return an item detail URL"""
    return reverse('item-detail-by-store', args=[store_id, pk])


# Helper function in our test for creating item
def create_item(**params):
    """Create and return a sample item"""
    defaults = {
        'name': 'Item Name'
    }
    defaults.update(params)

    item = Item.objects.create(**defaults)
    return item


def create_store(user, **params):
    """Create and return a sample store"""
    defaults = {
        'store_name': 'My Store',
        'important': True,
    }
    defaults.update(params)

    store = Store.objects.create(user=user, **defaults)
    return store


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicItemApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        # A test client that we can use for test
        # added to this class
        self.client = APIClient()

    def test_auth_required_item_api(self):
        """Test auth is required for item API"""
        user = create_user(email='user@test.com', password='test123')
        store = create_store(user)
        url = item_url(store.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_item_detail_api(self):
        """Test auth is required for item detail API"""
        user = create_user(email='user@test.com', password='test123')
        store = create_store(user=user)
        item = create_item(store_id=store.id)
        url = item_detail_url(store_id=store.id, pk=item.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemApiTests(TestCase):
    """Test authenticated api requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@test.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_get_request_items(self):
        """Test retrieving a list of items"""
        store = create_store(user=self.user)

        create_item(store_id=store.id)
        create_item(store_id=store.id)

        url = item_url(store.id)
        payload = {'store_id': store.id}
        res = self.client.get(url, payload)

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_item_list_limited_to_a_store(self):
        """Test list of items is limited to store"""
        other_user = create_user(email='other@test.com', password='test123')
        create_store(user=other_user)
        store = create_store(user=self.user)

        create_item(store_id=store.id)
        create_item(store_id=store.id)

        url = item_url(store_id=store.id)
        res = self.client.get(url)

        items = Item.objects.filter(store_id=store.id)
        serializer = ItemSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_item_detail(self):
        """Test get item detail"""
        store = create_store(user=self.user)
        item = create_item(store_id=store.id)

        url = item_detail_url(store_id=store.id, pk=item.id)
        res = self.client.get(url)

        serializer = ItemSerializer(item)
        self.assertEqual(res.data, serializer.data)

    def test_create_item(self):
        """Test creating a item"""
        store = create_store(user=self.user)
        payload = {
            'name': 'Item Name',
            'store': store.id
        }
        url = item_url(store_id=store.id)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        item = Item.objects.get(id=res.data['id'])
        self.assertEqual(item.name, payload['name'])
        self.assertEqual(item.store.id, store.id)

    def test_partial_update(self):
        """Test partial update of a item"""
        item_name = 'My Item'
        store = create_store(user=self.user)
        item = create_item(store_id=store.id, name=item_name)

        payload = {'name': 'New Item Name'}
        url = item_detail_url(store_id=store.id, pk=item.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, payload['name'])
        self.assertEqual(store.user, self.user)
        self.assertNotEqual(item.name, item_name)

    def test_full_update(self):
        """Test full update of item"""
        item_name = 'My Item'
        store = create_store(user=self.user)
        item = create_item(store_id=store.id, name=item_name)

        payload = {'name': 'New Item Name', 'store': store.id}
        url = item_detail_url(store_id=store.id, pk=item.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, payload['name'])
        self.assertEqual(store.user, self.user)
        self.assertEqual(item.store.id, store.id)
        self.assertNotEqual(item.name, item_name)

    def test_update_store_id_for_item_returns_error(self):
        """Test changing the item store results in an error"""
        item_name = 'My Item'
        store_1 = create_store(user=self.user)
        store_2 = create_store(user=self.user)
        item = create_item(store_id=store_1.id, name=item_name)

        payload = {'store_id': store_2.id}
        url = item_detail_url(store_id=store_2.id, pk=item.id)
        res = self.client.patch(url, payload)

        item.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(item.store.id == store_2.id)

    def test_delete_item(self):
        """Test deleting an item successful"""
        store = create_store(user=self.user)
        item = create_item(store_id=store.id)

        url = item_detail_url(store_id=store.id, pk=item.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=store.id).exists())

    def test_delete_other_store_item_error(self):
        """Test trying to delete another store item gives error"""
        item_name = 'My Item'
        store_1 = create_store(user=self.user)
        store_2 = create_store(user=self.user)
        item = create_item(store_id=store_2.id, name=item_name)

        url = item_detail_url(store_id=store_1.id, pk=item.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Item.objects.filter(store=store_2.id).exists())
