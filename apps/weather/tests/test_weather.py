
from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.tasks.models import Task


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

    def testIndex(self):
        response = self.client.get('/weather/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('weather'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/content.html')
        self.assertIn(':', response.context['current']['sunrise'])
