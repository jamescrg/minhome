
from pprint import pprint

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from app.models import Folder


class FoldersModelTests(TestCase):

    def setUp(self):
        Folder.objects.create(
                user_id=1,
                page='favorites',
                name='Main',
                home_column=1,
                home_rank=1,
                selected=1,
                active=1,
                )

    def testFolderContent(self):
        folder = Folder.objects.get(name='Main')
        expectedValues = {
            'user_id': 1,
            'page': 'favorites',
            'name': 'Main',
            'home_column': 1,
            'home_rank': 1,
            'selected': 1,
            'active': 1,
        }
        for key, val in expectedValues.items():
            with self.subTest(key=key, val=val):
                self.assertEqual(getattr(folder, key), val)

    def testContactString(self):
        folder = Folder.objects.get(name='Main')
        self.assertEqual(str(folder), f'{folder.name} : {folder.id}')
