from tempfile import NamedTemporaryFile

from PIL import Image
from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient

from core.models import UserModel
import mock
from django.core.files import File

file_mock = mock.MagicMock(spec=File, name='FileMock')


class TestUserView(TestCase):

    def test_api_returns_zero_users_when_no_users_exist(self):
        client = APIClient()
        response = client.get('/users/', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_api_returns_one_user(self):

        UserModel.objects.create_user(
            username='elias',
            email='elias@google.com',
            password='randomg@#@'
        )

        client = APIClient()
        response = client.get('/users/', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_api_returns_user_with_correct_values(self):

        UserModel.objects.create_user(
            username='elias',
            email='elias@google.com',
            password='randomg@#@',
            avatar=File(open("core/django.png", 'rb'))
        )
        client = APIClient()
        response = client.get('/users/', HTTP_ACCEPT='application/json')
        self.assertEqual(response.data[0].get('username'), 'elias')
        self.assertEqual(response.data[0].get('email'), 'elias@google.com')
        self.assertEqual(len(response.data[0]), 2)

    def test_model_saves_image_when_provided(self):
        UserModel.objects.create_user(
            username='elias',
            email='elias@google.com',
            password='randomg@#@',
            avatar=File(open("core/django.png", 'rb'))
        )

        user = UserModel.objects.last()

        open(user.avatar.name)
        self.assertIsNotNone(user.avatar.name)
