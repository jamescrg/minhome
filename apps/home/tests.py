from pprint import pprint

from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.favorites.models import Favorite


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
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


class HomeFolderTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')
        self.folders = [
            # column 1
            {
                'name': 'Main',
                'home_column': 1,
                'home_rank': 1,
            },
            {
                'name': 'Entertainment',
                'home_column': 1,
                'home_rank': 2,
            },
            {
                'name': 'Local',
                'home_column': 1,
                'home_rank': 3,
            },
            {
                'name': 'Social',
                'home_column': 1,
                'home_rank': 4,
            },
            # column 2
            {
                'name': 'Dev',
                'home_column': 2,
                'home_rank': 1,
            },
            {
                'name': 'Research',
                'home_column': 2,
                'home_rank': 2,
            },
            {
                'name': 'Filing',
                'home_column': 2,
                'home_rank': 3,
            },
            {
                'name': 'Food',
                'home_column': 2,
                'home_rank': 4,
            },
            # column 3
            {
                'name': 'Philosophy',
                'home_column': 3,
                'home_rank': 1,
            },
            {
                'name': 'Psych',
                'home_column': 3,
                'home_rank': 2,
            },
            {
                'name': 'History',
                'home_column': 3,
                'home_rank': 3,
            },
            {
                'name': 'Math',
                'home_column': 3,
                'home_rank': 4,
            },
            # column 4
            {
                'name': 'Physics',
                'home_column': 4,
                'home_rank': 1,
            },
            {
                'name': 'Anthro',
                'home_column': 4,
                'home_rank': 2,
            },
            {
                'name': 'Chorus',
                'home_column': 4,
                'home_rank': 3,
            },
            {
                'name': 'Annoying',
                'home_column': 4,
                'home_rank': 4,
            },
        ]
        for folder in self.folders:
            Folder.objects.create(
                user_id=self.user.id,
                name=folder['name'],
                home_column=folder['home_column'],
                home_rank=folder['home_rank'],
                page='favorites',
            )
        for i in range(1, 6):
            Favorite.objects.create(
                user_id=self.user.id,
                folder_id=1,
                name=f'Favorite No. {i}',
                description=f'Awesome {i}',
                home_rank=i,
            )

    def test_redirect(self):
        response = self.client.get('/home/folder/4/up/')
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get('/home/folder/4/up/')
        self.assertEqual(response.status_code, 302)

    def test_up_from_bottom(self):
        response = self.client.get('/home/folder/4/up/')
        folder = Folder.objects.get(pk=4)
        self.assertEqual(folder.home_rank, 3)
        folder = Folder.objects.get(pk=3)
        self.assertEqual(folder.home_rank, 4)

    def test_up_from_middle(self):
        response = self.client.get('/home/folder/3/up/')
        folder = Folder.objects.get(pk=3)
        self.assertEqual(folder.home_rank, 2)

    def test_up_from_top(self):
        response = self.client.get('/home/folder/1/up/')
        folder = Folder.objects.get(pk=1)
        self.assertEqual(folder.home_rank, 1)
        folder = Folder.objects.get(pk=2)
        self.assertEqual(folder.home_rank, 2)

    def test_down_from_bottom(self):
        response = self.client.get('/home/folder/16/down/')
        folder = Folder.objects.get(pk=16)
        self.assertEqual(folder.home_rank, 4)
        folder = Folder.objects.get(pk=15)
        self.assertEqual(folder.home_rank, 3)

    def test_down_from_middle(self):
        response = self.client.get('/home/folder/10/down/')
        folder = Folder.objects.get(pk=10)
        self.assertEqual(folder.home_rank, 3)
        folder = Folder.objects.get(pk=11)
        self.assertEqual(folder.home_rank, 2)

    def test_down_from_top(self):
        response = self.client.get('/home/folder/13/down/')
        folder = Folder.objects.get(pk=13)
        self.assertEqual(folder.home_rank, 2)
        folder = Folder.objects.get(pk=14)
        self.assertEqual(folder.home_rank, 1)

    def test_down_from_top_to_bottom(self):
        response = self.client.get('/home/folder/1/down/')
        response = self.client.get('/home/folder/1/down/')
        response = self.client.get('/home/folder/1/down/')
        folder = Folder.objects.get(pk=1)
        self.assertEqual(folder.home_rank, 4)
        folder = Folder.objects.get(pk=4)
        self.assertEqual(folder.home_rank, 3)

    def test_left_from_far_left(self):
        response = self.client.get('/home/folder/1/left/')
        folder = Folder.objects.get(pk=1)
        self.assertEqual(folder.home_column, 1)

    def test_left_from_middle_left(self):
        response = self.client.get('/home/folder/5/left/')
        folder = Folder.objects.get(pk=5)
        self.assertEqual(folder.home_column, 1)
        self.assertEqual(folder.home_rank, 5)

    def test_right_from_middle_right(self):
        response = self.client.get('/home/folder/9/right/')
        folder = Folder.objects.get(pk=9)
        self.assertEqual(folder.home_column, 4)
        self.assertEqual(folder.home_rank, 5)

    def test_right_from_far_right(self):
        response = self.client.get('/home/folder/13/right/')
        folder = Folder.objects.get(pk=13)
        self.assertEqual(folder.home_column, 4)

    def favorite_up_from_bottom(self):
        response = self.client.get('/home/favorite/5/up/')
        favorite = Favorite.objects.get(pk=5)
        self.assertEqual(favorite.home_rank, 4)
        favorite = Favorite.objects.get(pk=4)
        self.assertEqual(favorite.home_rank, 5)

    def favorite_up_from_top(self):
        response = self.client.get('/home/favorite/1/up/')
        favorite = Favorite.objects.get(pk=1)
        self.assertEqual(favorite.home_rank, 1)

    def favorite_down_from_bottom(self):
        response = self.client.get('/home/favorite/5/down/')
        favorite = Favorite.objects.get(pk=5)
        self.assertEqual(favorite.home_rank, 5)

    def favorite_down_from_bottom(self):
        response = self.client.get('/home/favorite/1/down/')
        favorite = Favorite.objects.get(pk=1)
        self.assertEqual(favorite.home_rank, 2)
        favorite = Favorite.objects.get(pk=2)
        self.assertEqual(favorite.home_rank, 1)
