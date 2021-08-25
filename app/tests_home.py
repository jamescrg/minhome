from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import Folder


class HomeViewTests(TestCase):

    def setUp(self):
        folderNames = [
            'Main',
            'Enterainment',
            'Python Tips',
            'Japanese',
            'Magic Mountain',
        ]
        for fname in folderNames:
            Folder.objects.create(name=fname, user_id=1)

    def test_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_url(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_named_route(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_uses_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/index.html')

    def test_folder_content(self):
        folder = Folder.objects.get(pk=5)
        expectedName = f'{folder.name}'
        self.assertEqual(expectedName, 'Magic Mountain')
