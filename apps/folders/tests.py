
from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from apps.folders.models import Folder


class ModelTests(TestCase):

    def setUp(self):
        Folder.objects.create(
            user_id=1,
            page='favorites',
            name='Main',
            home_column=1,
            home_rank=1,
            selected=1,
            active=1,
        )

    def testContent(self):
        folder = Folder.objects.get(name='Main')
        expectedValues = {
            'user_id': 1,
            'page': 'favorites',
            'name': 'Main',
            'home_column': 1,
            'home_rank': 1,
            'selected': 1,
            'active': 1,
        }
        for key, val in expectedValues.items():
            with self.subTest(key=key, val=val):
                self.assertEqual(getattr(folder, key), val)

    def testString(self):
        folder = Folder.objects.get(name='Main')
        self.assertEqual(str(folder), f'{folder.name}')


class ViewTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

        folders = [
            'Social',
            'Recipes',
            'Places',
            'Philosophy',
        ]

        for name in folders:
            user_id = self.user.id
            Folder.objects.create(
                user_id=user_id, page='notes', name=name, home_column=0, home_rank=0
            )

    def testHome(self):
        response = self.client.get('/folders/home/4/notes')
        self.assertEqual(response.status_code, 302)
        folder = Folder.objects.filter(pk=4).get()
        self.assertEqual(folder.home_column, 4)
        self.assertEqual(folder.home_rank, 1)

    def testSelect(self):
        response = self.client.get('/folders/4/notes')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/notes/')
        self.assertContains(response, 'Philosophy')

    def testInsert(self):
        data = {
            'user_id': 1,
            'folder_id': 2,
            'page': 'notes',
            'name': 'Existentialism',
        }

        response = self.client.post('/folders/insert/notes', data)
        self.assertEqual(response.status_code, 302)
        found = Folder.objects.filter(name='Existentialism').exists()
        self.assertTrue(found)

    def testUpdate(self):
        data = {
            'user_id': self.user.id,
            'folder_id': 4,
            'page': 'notes',
            'name': 'Existentialism',
        }

        response = self.client.post('/folders/update/4/notes', data)
        self.assertEqual(response.status_code, 302)
        found = Folder.objects.filter(name='Existentialism').exists()
        self.assertTrue(found)

    def testDelete(self):
        response = self.client.get('/folders/delete/4/notes')
        found = Folder.objects.filter(name='Philosophy').exists()
        self.assertFalse(found)
