
from pprint import pprint

from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse
from django.urls import resolve
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from app.models import Folder, Note


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


    def testString(self):
        note = Note.objects.get(subject='notes')
        self.assertEqual(str(note), f'{note.subject} : {note.id}')


class ViewTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
                'john', 'lennon@thebeatles.com', 'johnpassword')
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
                    user_id=user_id,
                    page='notes',
                    name=name,
                    )


        notes = [
            'Socrates',
            'Kant',
            'Mill',
            'Nietzsche',
        ]

        for subject in notes:
            Note.objects.create(
                    user_id=user_id,
                    folder_id=4,
                    subject=subject,
                    note='Some text here',
                    )


    def testIndexView(self):
        response = self.client.get('/notes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'notes')
        self.assertTemplateUsed(response, 'notes/content.html')
        self.assertContains(response, 'Philosophy')


    def testSelectFolder(self):
        folders = Folder.objects.all()
        response = self.client.get('/folders/4/notes')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/notes/')
        self.assertEqual(response.context['page'], 'notes')
        self.assertTemplateUsed(response, 'notes/content.html')
        self.assertContains(response, 'Philosophy')
        self.assertContains(response, 'Nietzsche')
