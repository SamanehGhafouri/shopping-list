"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


# helper for items
def create_user(email='user@test.com', password='user123'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_and_password(self):
        email = 'user@test.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_without_email_raises_error(self):
        """Test the creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'user@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_normalized_email(self):
        emails = [
            ['user1@TEST.com', 'user1@test.com'],
            ['user2@Test.com', 'user2@test.com'],
            ['USER3@TEST.COM', 'USER3@test.com'],
            ['user4@test.Com', 'user4@test.com'],
        ]
        for actual_email, expected_email in emails:
            user = get_user_model().objects.create_user(
                actual_email, 'test123'
                )
            self.assertEqual(user.email, expected_email)

    def test_create_store(self):
        user = get_user_model().objects.create_user(
            'user@test.com',
            'user123',
        )
        store = models.Store.objects.create(
            user=user,
            store_name='My Store',
            created='2023-08-01T23:46:26.226Z',
            important=True
        )
        self.assertEqual(str(store), store.store_name)

    def test_create_item(self):
        user = create_user()
        store = models.Store.objects.create(
            user=user,
            store_name='My Store',
            created='2023-08-01T23:46:26.226Z',
            important=True
        )
        item = models.Item.objects.create(store=store, name='Bread')
        self.assertEqual(str(item), item.name)
