
from pprint import pprint

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from app.models import Folder


class HomeViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def testBaseUrl(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def testHomeUrl(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def testNamedRoute(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/index.html')
