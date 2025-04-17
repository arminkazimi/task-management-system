from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Project
from tasks.models import Task

User = get_user_model()

class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.project_data = {
            'name': 'Test Project',
            'description': 'Test Project Description',
            'owner': self.user
        }
        self.project = Project.objects.create(**self.project_data)

    def test_create_project(self):
        """Test creating a new project"""
        self.assertEqual(self.project.name, self.project_data['name'])
        self.assertEqual(self.project.description, self.project_data['description'])
        self.assertEqual(self.project.owner, self.project_data['owner'])

    def test_add_task_to_project(self):
        """Test adding a task to project"""
        task = Task.objects.create(
            title='Project Task',
            description='Task for project',
            status='TODO',
            priority='HIGH',
            assigned_to=self.user,
            project=self.project
        )
        self.assertEqual(self.project.tasks.count(), 1)
        self.assertEqual(self.project.tasks.first(), task)

class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project_data = {
            'name': 'API Test Project',
            'description': 'API Test Project Description'
        }

    def test_create_project_api(self):
        """Test creating project through API"""
        response = self.client.post('/api/projects/', self.project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, self.project_data['name'])

    def test_list_projects_api(self):
        """Test listing projects through API"""
        Project.objects.create(**self.project_data, owner=self.user)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
