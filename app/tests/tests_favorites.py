
from pprint import pprint

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from app.models import Favorite


class FavoritesViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
                'john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def testUrls(self):
        urls = [
            '/favorites/',
            '/favorites/add/10000',
            '/favorites/insert/',
            'favorites/eit/10000',
            'favorites/update/10000',
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def testNamedRoute(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('favorites'))
        self.assertTemplateUsed(response, 'favorites/content.html')


class FavoritesModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
                'john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        Favorite.objects.create(
                user_id=1,
                folder_id=1,
                name='Meditation Posture',
                url='http://meditationposture.net',
                description='A website',
                login='drachma',
                root='rupee',
                passkey='ruble',
                selected=1,
                )

    def testFavorite(self):
        favorite = Favorite.objects.get(name="Meditation Posture")
        expectedValues = {
            'user_id': 1,
            'folder_id': 1,
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
        self.assertEqual(str(favorite), f'{favorite.name} : {favorite.id}')


