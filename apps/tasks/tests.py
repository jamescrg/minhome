
from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.tasks.models import Task


class ModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

        folder1 = Folder.objects.create(
            user_id=1,
            page='tasks',
            name='Todo',
        )

        Task.objects.create(
            user_id=1,
            folder_id=folder1.id,
            title='Do this today',
            status=1,
        )

    def testContent(self):
        folder = Folder.objects.all().first()
        task = Task.objects.all().first()
        expectedValues = {
            'user_id': 1,
            'folder_id': folder.id,
            'title': 'Do this today',
            'status': 1,
        }
        for key, val in expectedValues.items():
            with self.subTest(key=key, val=val):
                self.assertEqual(getattr(task, key), val)

    def testString(self):
        folder = Folder.objects.all().first()
        task = Task.objects.get(folder_id=folder.id)
        self.assertEqual(str(task), f'{task.title} : {task.id}')


class ViewTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

        folders = [
            'Current',
            'Chores',
            'Writing',
            'Monday',
        ]

        for name in folders:
            user_id = self.user.id
            Folder.objects.create(
                user_id=user_id,
                page='tasks',
                name=name,
            )

        tasks = [
            'Take out trash',
            'Rake leaves',
            'Sweep back porch',
            'Scrub shower tile',
        ]

        for title in tasks:
            Task.objects.create(
                user_id=user_id,
                folder_id=2,
                title=title,
                status=0,
            )

    def testIndex(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('tasks'))
        self.assertTemplateUsed(response, 'tasks/content.html')

    def testActivate(self):
        response = self.client.get('/tasks/2/activate')
        self.assertEqual(response.status_code, 302)
        folder = Folder.objects.filter(pk=2).get()
        self.assertEqual(folder.active, 1)

    def testStatus(self):
        response = self.client.get('/tasks/2/complete')
        self.assertEqual(response.status_code, 302)
        task = Task.objects.filter(pk=2).get()
        self.assertEqual(task.status, 1)

    def testAddData(self):
        data = {
            'user_id': 1,
            'folder_id': 3,
            'title': 'Sweep garage',
        }

        response = self.client.post('/tasks/add', data)
        self.assertEqual(response.status_code, 302)
        found = Task.objects.filter(folder_id=3).exists()
        self.assertTrue(found)

    def testEdit(self):
        response = self.client.get('/tasks/4/edit')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'tasks')
        self.assertTemplateUsed(response, 'tasks/form.html')

    def testEditData(self):
        data = {
            'user_id': self.user.id,
            'folder_id': 3,
            'title': 'Sweep garage',
        }

        response = self.client.post('/tasks/2/edit', data)
        self.assertEqual(response.status_code, 302)
        found = Task.objects.filter(title='Sweep garage').exists()
        self.assertTrue(found)

    def testClear(self):
        tasks = Task.objects.filter(folder_id=2).update(status=1)
        response = self.client.get('/tasks/2/clear')
        tasks = Task.objects.filter(folder_id=2)
        self.assertFalse(tasks)
