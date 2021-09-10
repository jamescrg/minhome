
from pprint import pprint

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from app.models import Note


class NotesViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
                'john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def testUrl(self):
        response = self.client.get('/notes/')
        self.assertEqual(response.status_code, 200)

    def testNamedRoute(self):
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('notes'))
        self.assertTemplateUsed(response, 'notes/content.html')


class NotesModelTests(TestCase):

    def setUp(self):
        Note.objects.create(
                user_id=1,
                folder_id=1,
                subject='notes',
                note='Main',
                selected=1,
                )

    def testNoteContent(self):
        note = Note.objects.get(subject='notes')
        expectedValues = {
            'user_id': 1,
            'folder_id': 1,
            'subject': 'notes',
            'note': 'Main',
            'selected': 1,
        }
        for key, val in expectedValues.items():
            with self.subTest(key=key, val=val):
                self.assertEqual(getattr(note, key), val)

    def testContactString(self):
        note = Note.objects.get(subject='notes')
        self.assertEqual(str(note), f'{note.subject} : {note.id}')
