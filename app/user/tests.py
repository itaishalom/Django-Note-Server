from rest_framework.authtoken.admin import User
from .serializers import UserSerializer
from rest_framework.test import APITestCase
from rest_framework import status


class UserSerializerTestCase(APITestCase):
    def test_create_user(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }

        serializer = UserSerializer(data=user_data)

        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.email, user_data['email'])


class UserCreateViewTestCase(APITestCase):
    def test_create_user_success(self):
        user_data = {'username': 'testuser', 'password': 'testpassword',
                     'email': 'test@example.com'}
        user_data_reply = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post(self.create_path(), user_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, user_data_reply)

    def test_create_user_invalid_data(self):
        invalid_user_data = {'username': 'testuser', 'email': 'invalidemail'}

        response = self.client.post(self.create_path(), invalid_user_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('password', response.data)

    def create_path(self):
        return '/users/add/'


class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword',
                                             email='test@example')

    def test_login_success(self):
        login_data = {'username': 'testuser', 'password': 'testpassword'}

        # Make a POST request to login API
        response = self.client.post(self.login_path(), data=login_data)
        # Check if login is successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertIn('token', response.data)

    def login_path(self):
        return '/users/login/'

    def test_login_invalid_credentials(self):
        # Invalid login credentials
        invalid_login_data = {'username': 'testuser',
                              'password': 'invalidpassword'}

        # Make a POST request to login API with invalid credentials
        response = self.client.post(self.login_path(), invalid_login_data,
                                    format='json')

        # Check if login fails with 400 Bad Request status
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)

    def test_login_invalid_method(self):
        # Make a GET request to login API (invalid method)
        response = self.client.get(self.login_path())

        # Check if the response status is 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
