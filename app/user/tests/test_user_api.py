from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factories import UserFactory


class BaseUser(APITestCase):
    """Basic set up class"""

    def setUp(self):
        self.current_user = UserFactory.create()
        self.foreign_user = UserFactory.create()
        self.superuser = UserFactory.create(is_superuser=True)
        self.inactive = UserFactory.create(is_active=False)


class UserListTest(BaseUser):
    """Users list, create tests collection"""

    @property
    def url(self):
        """Method returns URL to user list endpoint"""
        return reverse('users-list')

    def test_url(self):
        """Ensure url is resolved properly"""
        self.assertEqual(self.url, '/users/')

    def test_success_list(self):
        """Ensure list is fetched properly"""
        self.client.force_authenticate(self.current_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_anonymous_fails_list(self):
        """Ensure anonymous user can not list"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_fails_create(self):
        """Ensure anonymous user can not create"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserReadUpdateTest(BaseUser):
    """Users list tests collection"""

    @property
    def url(self):
        """Method returns URL to user list endpoint"""
        return reverse('users-detail', args=[str(self.current_user.pk)])

    def test_url(self):
        """Ensure url is resolved properly"""
        self.assertEqual(self.url, f'/users/{self.current_user.pk}/')

    def test_success_read(self):
        """Ensure entry is read properly"""
        self.client.force_authenticate(self.current_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.current_user.username, response.data['username'])
        self.assertEqual(self.current_user.email, response.data['email'])
        self.assertEqual(self.current_user.first_name, response.data['first_name'])
        self.assertEqual(self.current_user.last_name, response.data['last_name'])

    def test_fail_read_foreign(self):
        """Ensure entry is read properly"""
        self.client.force_authenticate(self.foreign_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_read_anonymous(self):
        """Ensure entry is read properly"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_update(self):
        """Ensure entry is updated properly"""
        self.client.force_authenticate(self.current_user)
        context = {
            'username': f'changed_{self.current_user.username}',
            'email': f'changed_{self.current_user.email}',
            'first_name': f'changed_{self.current_user.first_name}',
            'last_name': f'changed_{self.current_user.last_name}',
        }
        response = self.client.put(self.url, data=context)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.current_user.refresh_from_db()
        self.assertEqual(self.current_user.username, context['username'])
        self.assertEqual(self.current_user.email, context['email'])
        self.assertEqual(self.current_user.first_name, context['first_name'])
        self.assertEqual(self.current_user.last_name, context['last_name'])

    def test_foreign_fails_update(self):
        """Ensure user can not change foreign user"""
        self.client.force_authenticate(self.foreign_user)
        response = self.client.put(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_fails_update(self):
        """Ensure anonymous can not change user"""
        response = self.client.put(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_foreign_fails_delete(self):
        """Ensure user can not delete foreign user"""
        self.client.force_authenticate(self.foreign_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_anonymous_fails_delete(self):
        """Ensure anonymous can not delete user"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
