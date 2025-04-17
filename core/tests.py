from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Test creating a new user"""
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_user_email_normalized(self):
        """Test email is normalized for new user"""
        email = 'test@EXAMPLE.com'
        user = User.objects.create_user(email=email, password='test123')
        self.assertEqual(user.email, email.lower())

class UserAPITests(APITestCase):
    def setUp(self):
        self.create_url = '/api/users/'
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user_api(self):
        """Test creating user through API"""
        response = self.client.post(self.create_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data['email'])
