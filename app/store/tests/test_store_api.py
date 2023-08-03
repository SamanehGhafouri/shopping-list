"""
Tests for Store APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Store

from store.serializers import StoreSerializer


STORE_URL = reverse('store-list-view')


def store_detail_url(store_id):
    """Create and return a store detail URL"""
    return reverse('store-detail-view', args=[store_id])


# Helper function in our test for creating store
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


class PublicStoreApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        # A test client that we can use for test
        # added to this class
        self.client = APIClient()

    def test_auth_required_store_api(self):
        """Test auth is required for store API"""
        res = self.client.get(STORE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_store_detail_api(self):
        """Test auth is required for store detail API"""
        url = store_detail_url(1)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStoreApiTests(TestCase):
    """Test authenticated api requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@test.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_get_request_stores(self):
        """Test retrieving a list of stores"""
        create_store(user=self.user)
        create_store(user=self.user)

        res = self.client.get(STORE_URL)

        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_store_list_limited_to_user(self):
        """Test list of stores is limited to authenticated user"""
        other_user = create_user(email='other@test.com', password='test123')
        create_store(user=other_user)
        create_store(user=self.user)

        res = self.client.get(STORE_URL)

        stores = Store.objects.filter(user=self.user)
        serializer = StoreSerializer(stores, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_store_detail(self):
        """Test get store detail"""
        store = create_store(user=self.user)

        url = store_detail_url(store.id)
        res = self.client.get(url)

        serializer = StoreSerializer(store)
        self.assertEqual(res.data, serializer.data)

    def test_create_store(self):
        """Test creating a store"""
        payload = {
            'store_name': 'Store test',
            'important': True
        }
        res = self.client.post(STORE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        store = Store.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(store, k), v)
        self.assertEqual(store.user, self.user)

    def test_partial_update(self):
        """Test partial update of a store"""
        original_important = True
        store = create_store(
            user=self.user,
            store_name='My Store',
            important=original_important,
        )

        payload = {'store_name': 'New Store Name'}
        url = store_detail_url(store.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        store.refresh_from_db()
        self.assertEqual(store.store_name, payload['store_name'])
        self.assertEqual(store.important, original_important)
        self.assertEqual(store.user, self.user)

    def test_full_update(self):
        """Test full update of store"""
        store = create_store(
            user=self.user,
            store_name='My Store',
            important=True
        )

        payload = {
            'store_name': 'New updated store',
            'important': False
        }
        url = store_detail_url(store.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        store.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(store, k), v)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.store_name, payload['store_name'])
        self.assertEqual(store.important, payload['important'])

    def test_update_user_returns_error(self):
        """Test changing the store user results in an error"""
        new_user = create_user(email='user2@test.com', password='test123')
        store = create_store(user=self.user)

        payload = {'user': new_user}
        url = store_detail_url(store.id)
        self.client.patch(url, payload)

        store.refresh_from_db()
        self.assertEqual(store.user, self.user)

    def test_delete_store(self):
        """Test deleting a store successful"""
        store = create_store(user=self.user)

        url = store_detail_url(store.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Store.objects.filter(id=store.id).exists())

    def test_delete_other_users_store_error(self):
        """Test trying to delete another users store gives error"""
        new_user = create_user(email='user2@test.com', password='test123')
        store = create_store(user=new_user)

        url = store_detail_url(store.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Store.objects.filter(id=store.id).exists())
