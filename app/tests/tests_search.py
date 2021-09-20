
from pprint import pprint

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser
from app.models import Folder, Favorite, Note, Contact


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def testIndex(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('search'))
        self.assertTemplateUsed(response, 'search/content.html')
        self.assertTemplateUsed(response, 'search/form.html')

    def testResults(self):
        Favorite.objects.create(
                name='Google', 
                user_id=self.user.id,
                folder_id=1,
                description='Search enginge for james.'
                )
        Note.objects.create(
                subject='Tasks for James',
                folder_id=1,
                user_id=self.user.id,
                )
        Contact.objects.create(
                name='James Craig',
                folder_id=1,
                user_id=self.user.id,
                )
        data = {
            'search_text': 'James',
        }
        response = self.client.post('/search/results', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/content.html')
        self.assertTemplateUsed(response, 'search/results.html')

        favorites = response.context['favorites']
        favorite = favorites.filter(name='Google').get()
        self.assertEqual(favorite.name, 'Google')

        note = response.context['notes']
        note = note.filter(pk=1).get()
        self.assertEqual(note.subject, 'Tasks for James')

        contact = response.context['contacts']
        contact = contact.filter(name='James Craig').get()
        self.assertEqual(contact.name, 'James Craig')
