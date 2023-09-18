from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import os
from .models import Chrome
from authentication.models import CustomUser


class ChromeViewTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='password123',
        )

    def test_analyze_chrome(self):
        # Log in the user
        self.api_client.force_authenticate(user=self.user)
        res = os.path.expanduser("~")

        # Prepare data for the request
        data = {
            'pc_username': res.split('\\')[2],
            'user_id': self.user.id,
        }
        url = reverse('metadata:analyze')
        response = self.api_client.post(url, data, format='json')

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chrome_view(self):
        # Log in the user
        self.api_client.force_authenticate(user=self.user)
        data = {
            'pc_username': os.environ["USERPROFILE"],
            'user_id': self.user.id,
        }
        chrome_instance = Chrome.objects.create(user=self.user, pc_username=data['pc_username'])
        url = reverse('metadata:chrome_view', kwargs={'pk': chrome_instance.pk})
        response = self.api_client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
