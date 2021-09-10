
from pprint import pprint

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from app.models import Task


class TasksViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def testUrl(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def testNamedRoute(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('tasks'))
        self.assertTemplateUsed(response, 'tasks/content.html')


class TasksModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Task.objects.create(
                user_id=1,
                folder_id=10,
                title='Do this today',
                status=1,
                )

    def testTaskContent(self):
        task = Task.objects.get(pk=1)
        expectedValues = {
                'user_id': 1,
                'folder_id': 10,
                'title': 'Do this today',
                'status': 1,
        }
        for key, val in expectedValues.items():
            with self.subTest(key=key, val=val):
                self.assertEqual(getattr(task, key), val)

    def testContactString(self):
        task = Task.objects.get(pk=1)
        self.assertEqual(str(task), f'{task.title} : {task.id}')
