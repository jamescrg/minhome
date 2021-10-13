from pprint import pprint

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from apps.folders.models import Folder


class SettingsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

    def testUrl(self):
        response = self.client.get('/settings/')
        self.assertEqual(response.status_code, 200)

    def testNamedRoute(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('settings'))
        self.assertTemplateUsed(response, 'settings/content.html')
