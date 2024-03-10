from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIClient

from .models import Note
from .serializers import NoteSerializer
from django.test import TestCase
from rest_framework.authtoken.models import Token

from .utils import validate_user, generate_filter, calculate_word_count


class NoteSerializerTestCase(TestCase):
    def test_note_serializer(self):
        user = User.objects.create(username='test_user')

        note_data = {'title': 'Test Note', 'body': 'This is a test note',
                     'tags': ['tag1', 'tag2'], 'user': user}
        note = Note.objects.create(**note_data)

        serializer = NoteSerializer(instance=note)
        serialized_data = serializer.data

        self.assertEqual(serialized_data['title'], note_data['title'])
        self.assertEqual(serialized_data['body'], note_data['body'])
        self.assertEqual(serialized_data['tags'], note_data['tags'])

    def test_note_deserializer(self):
        serialized_data = {'title': 'Test Note', 'body': 'This is a test note',
                           'tags': ['tag1', 'tag2']}

        serializer = NoteSerializer(data=serialized_data)
        serializer.is_valid(raise_exception=True)
        deserialized_data = serializer.validated_data

        self.assertEqual(deserialized_data['title'], serialized_data['title'])
        self.assertEqual(deserialized_data['body'], serialized_data['body'])
        self.assertEqual(deserialized_data['tags'], serialized_data['tags'])


class NoteModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')

    def test_create_note(self):
        note = Note.objects.create(
            title='Test Title',
            body='Test Body',
            tags='tag1,tag2',
            user=self.user,
            privacy='public'
        )

        self.assertIsInstance(note, Note)
        self.assertEqual(note.title, 'Test Title')
        self.assertEqual(note.body, 'Test Body')
        self.assertEqual(note.tags, 'tag1,tag2')
        self.assertEqual(note.user, self.user)
        self.assertEqual(note.privacy, 'public')

    def test_str_method(self):
        note = Note.objects.create(
            title='Test Title',
            body='Test Body',
            tags='tag1,tag2',
            user=self.user,
            privacy='public'
        )
        self.assertEqual(str(note), 'Test Title')


class UserNotesViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.note_data = {'title': 'Test Note', 'body': 'This is a test note',
                          'tags': ['tag']}

    def test_post_method(self):
        response = self.client.post('/notes/', self.note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.get().title, 'Test Note')

    def test_get_method(self):
        response = self.client.get('/notes/', format='json')
        data = response.json()
        results = data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)

    def test_delete_method(self):
        note = Note.objects.create(title='Test Note',
                                   body='This is a test note', tags=['tag1'],
                                   user=self.user)
        response = self.client.delete(f'/notes/{note.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

    def test_put_method(self):
        note = Note.objects.create(title='Test Note',
                                   body='This is a test note', tags=['tag1'],
                                   user=self.user)
        updated_data = {'title': 'Updated Note',
                        'body': 'This note has been updated', 'tags': ['tag2']}
        response = self.client.put(f'/notes/{note.id}', updated_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_note = Note.objects.get(id=note.id)
        self.assertEqual(updated_note.title, 'Updated Note')


class UserPublicNotesViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_method(self):
        response = self.client.get('/notes/public/', format='json')
        data = response.json()
        results = data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)


class NoteUtilsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.note = Note.objects.create(title='Test Note',
                                        body='This is a test note',
                                        user=self.user)

    def test_validate_user(self):
        # Test valid user
        self.assertIsNone(validate_user(self.note, self.user))

        # Test invalid user
        invalid_user = User.objects.create_user(username='invaliduser',
                                                password='invalidpassword')
        with self.assertRaises(PermissionDenied):
            validate_user(self.note, invalid_user)

    def test_generate_filter(self):
        # Test with both query and tag
        filter_conditions = generate_filter('query', 'tag',
                                            Q(password__contains='pass'))

        self.assertTrue('tags__contains' in str(filter_conditions))
        self.assertTrue('body__icontains' in str(filter_conditions))
        self.assertTrue('password__contains' in str(filter_conditions))

        # Test with only test
        filter_conditions = generate_filter('', '',
                                            Q(test__contains='test', tag=None))
        self.assertFalse('body__icontains' in str(filter_conditions))
        self.assertTrue('test__contains' in str(filter_conditions))

    def test_calculate_word_count(self):
        content = "This is a test content."
        self.assertEqual(calculate_word_count(content), 5)

        content = ""
        self.assertEqual(calculate_word_count(content), 0)

        content = "Hello World!"
        self.assertEqual(calculate_word_count(content), 2)
