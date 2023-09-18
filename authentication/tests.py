from django.test import TestCase
from authentication.models import CustomUser
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.test import APIClient


#   User = get_user_model()


class AuthAPITests(TestCase):

    def setUp(self):
        self.api_client = APIClient()

    def test_create_user(self):
        url = reverse('authentication:register_user')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.api_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CustomUser.objects.filter(email=data['email']).exists())

    def test_create_user_duplicate(self):
        # Create a user with the same email first
        CustomUser.objects.create_user(email='test@example.com', password='password123')

        url = reverse('authentication:register_user')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.api_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('That email is already in use.', response.data['error_message'])

    #   def test_obtain_auth_token(self):
    #       user = CustomUser.objects.create_user(email='test@example.com', password='password123')

    # Attempt to obtain an authentication token for the user
    #       url = reverse('authentication:token_view')
    #    data = {
    #          'email': 'test@example.com',
    #           'password': 'password123',
    #       }
    #       res = self.api_client.post(url, data, format='json')

    #       self.assertEqual(res.status_code, status.HTTP_200_OK)
    #       self.assertIn('token', res.data)

    def test_all_users(self):
        user1 = CustomUser.objects.create_user(email='user1@example.com', password='password123', first_name='User1')
        user2 = CustomUser.objects.create_user(email='user2@example.com', password='password456', first_name='User2')

        url = reverse('authentication:users')
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        # Check that both user emails are in the response
        self.assertIn('user1@example.com', str(response.data))
        self.assertIn('user2@example.com', str(response.data))

    #   py manage.py test authentication.tests
