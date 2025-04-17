from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_home_page_unauthenticated(self):
        """Test home page for unauthenticated user"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Register')
        self.assertNotContains(response, 'View Projects')

    def test_home_page_authenticated(self):
        """Test home page for authenticated user"""
        self.client.force_login(self.user)
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertContains(response, 'View Projects')
        self.assertContains(response, 'View Tasks')
        self.assertContains(response, 'Logout')
        self.assertNotContains(response, 'Login')
