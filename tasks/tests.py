from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

User = get_user_model()

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'TODO',
            'priority': 'MEDIUM',
            'assigned_to': self.user
        }
        self.task = Task.objects.create(**self.task_data)

    def test_create_task(self):
        """Test creating a new task"""
        self.assertEqual(self.task.title, self.task_data['title'])
        self.assertEqual(self.task.description, self.task_data['description'])
        self.assertEqual(self.task.status, self.task_data['status'])
        self.assertEqual(self.task.priority, self.task_data['priority'])
        self.assertEqual(self.task.assigned_to, self.task_data['assigned_to'])

    def test_task_status_update(self):
        """Test updating task status"""
        self.task.status = 'IN_PROGRESS'
        self.task.save()
        self.assertEqual(self.task.status, 'IN_PROGRESS')

class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.task_data = {
            'title': 'API Test Task',
            'description': 'API Test Description',
            'status': 'TODO',
            'priority': 'HIGH'
        }

    def test_create_task_api(self):
        """Test creating task through API"""
        response = self.client.post('/api/tasks/', self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, self.task_data['title'])

    def test_list_tasks_api(self):
        """Test listing tasks through API"""
        Task.objects.create(**self.task_data, assigned_to=self.user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
