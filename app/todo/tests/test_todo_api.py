from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todo.tests.factories import TaskFactory
from user.tests.factories import UserFactory


class BaseTask(APITestCase):
    """Basic set up class"""

    def setUp(self):
        self.current_user = UserFactory.create()
        self.first_task = TaskFactory.create(owner=self.current_user)
        self.second_task = TaskFactory.create(owner=self.current_user)

        self.foreign_user = UserFactory.create()
        self.foreign_task = TaskFactory.create(owner=self.foreign_user)


class TaskListTest(BaseTask):
    """Task list, create tests collection"""

    @property
    def url(self):
        """Method returns URL to tasks list endpoint"""
        return reverse('tasks-list')

    def test_url(self):
        """Ensure url is resolved properly"""
        self.assertEqual(self.url, '/todos/')

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

    def test_success_create(self):
        """Ensure entry is updated properly"""
        self.client.force_authenticate(self.current_user)
        context = {
            'name': 'task name',
            'description': 'task description',
            'status': 'pending',
        }
        response = self.client.post(self.url, data=context)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_fails_create(self):
        """Ensure anonymous user can not create"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskReadUpdateTest(BaseTask):
    """Tasks list tests collection"""

    @property
    def url(self):
        """Method returns URL to tasks list endpoint"""
        return reverse('tasks-detail', args=[str(self.first_task.pk)])

    def test_url(self):
        """Ensure url is resolved properly"""
        self.assertEqual(self.url, f'/todos/{self.first_task.pk}/')

    def test_success_read(self):
        """Ensure entry is read properly"""
        self.client.force_authenticate(self.current_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.first_task.name, response.data['name'])
        self.assertEqual(self.first_task.description, response.data['description'])
        self.assertEqual(self.first_task.status, response.data['status'])

    def test_fail_read_foreign(self):
        """Ensure entry is read properly"""
        self.client.force_authenticate(self.foreign_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_read_anonymous(self):
        """Ensure entry is read properly"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_update(self):
        """Ensure entry is updated properly"""
        self.client.force_authenticate(self.current_user)
        context = {
            'name': f'changed_{self.first_task.name}',
            'description': f'changed_{self.first_task.description}',
            'status': 'finished',
        }
        response = self.client.put(self.url, data=context)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.first_task.refresh_from_db()
        self.assertEqual(self.first_task.name, response.data['name'])
        self.assertEqual(self.first_task.description, response.data['description'])
        self.assertEqual(self.first_task.status, response.data['status'])

    def test_foreign_fails_update(self):
        """Ensure user can not change foreign task"""
        self.client.force_authenticate(self.foreign_user)
        response = self.client.put(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_fails_update(self):
        """Ensure anonymous can not change task"""
        response = self.client.put(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_delete(self):
        """Ensure user can delete task"""
        self.client.force_authenticate(self.current_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_foreign_fails_delete(self):
        """Ensure user can not delete foreign task"""
        self.client.force_authenticate(self.foreign_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_fails_delete(self):
        """Ensure anonymous can not delete user"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
