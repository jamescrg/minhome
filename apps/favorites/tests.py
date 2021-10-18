
from pprint import pprint

from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.favorites.models import Favorite


class ModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

        folder1 = Folder.objects.create(
            user_id=1,
            page='favorites',
            name='Meditation',
        )

        Favorite.objects.create(
            user_id=1,
            folder_id=folder1.id,
            name='Meditation Posture',
            url='http://meditationposture.net',
            description='A website',
            login='drachma',
            root='rupee',
            passkey='ruble',
            selected=1,
        )

    def testFavorite(self):
        folder = Folder.objects.all().first()
        favorite = Favorite.objects.get(name="Meditation Posture")
        expectedValues = {
            'user_id': 1,
            'folder_id': folder.id,
            'name': 'Meditation Posture',
            'url': 'http://meditationposture.net',
            'description': 'A website',
            'login': 'drachma',
            'root': 'rupee',
            'passkey': 'ruble',
            'selected': 1,
        }
        for key, val in expectedValues.items():
            with self.subTest(key=key, val=val):
                self.assertEqual(getattr(favorite, key), val)

    def testFavoriteString(self):
        favorite = Favorite.objects.get(name="Meditation Posture")
        self.assertEqual(str(favorite), f'{favorite.name}')


class ViewTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

        folders = [
            'Main',
            'Dev',
            'Fun',
            'Local',
        ]

        for name in folders:
            user_id = self.user.id
            Folder.objects.create(
                user_id=user_id,
                page='favorites',
                name=name,
            )

        Folder.objects.filter(name='Local').update(selected=1)

        first_folder = Folder.objects.all().first()

        favorites = [
            {
                'name': 'Google',
                'url': 'https://go.com',
            },
            {
                'name': 'Yahoo',
                'url': 'https://go.com',
            },
            {
                'name': 'Bing',
                'url': 'https://go.com',
            },
        ]

        for favorite in favorites:
            Favorite.objects.create(
                user_id=1,
                folder_id=first_folder.id,
                selected=0,
                name=favorite['name'],
                url=favorite['url'],
            )

    def testIndex(self):
        response = self.client.get('/favorites/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('favorites'))
        self.assertTemplateUsed(response, 'favorites/content.html')

    def testAdd(self):
        response = self.client.get('/favorites/add')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites/form.html')

    def testAddData(self):
        data = {
            'folder': 4,
            'name': 'Reddit',
            'url': 'https://reddit.com',
        }

        response = self.client.post('/favorites/add', data)
        self.assertEqual(response.status_code, 302)
        found = Favorite.objects.filter(name='Reddit').exists()
        self.assertTrue(found)

    def testEdit(self):
        response = self.client.get('/favorites/2/edit')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites/form.html')

    def testEditData(self):
        data = {
            'folder': 4,
            'name': 'Reddit',
            'url': 'https://reddit.com',
        }

        response = self.client.post('/favorites/2/edit', data)
        self.assertEqual(response.status_code, 302)
        found = Favorite.objects.filter(name='Reddit').exists()
        self.assertTrue(found)

    def testDelete(self):
        response = self.client.get('/favorites/delete/3')
        self.assertEqual(response.status_code, 302)
        found = Favorite.objects.filter(name='Bing').exists()
        self.assertFalse(found)

    def testHome(self):
        response = self.client.get('/favorites/home/2')
        self.assertEqual(response.status_code, 302)
        favorite = Favorite.objects.filter(pk=2).get()
        self.assertEqual(favorite.home_rank, 1)
