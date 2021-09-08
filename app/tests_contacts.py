
from pprint import pprint

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from app.models import Contact, Folder


class ContactsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
                'john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        Contact.objects.create(
                user_id=1,
                folder_id=1,
                selected=1,
                name='Mohandas Gandhi',
                company='Gandhi, PC',
                address='225 Paper Street, Porbandar, India',
                phone1='123.456.7890',
                phone1_label='Work',
                email='gandhi@gandhi.com',
                website='gandhi.com',
                notes='The Mahatma'
                )

    def testContactsUrl(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def testNamedRoute(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('contacts'))
        self.assertTemplateUsed(response, 'contacts/content.html')

    def testContactContent(self):
        contact = Contact.objects.get(id=1)
        expectedValues = {
            'name': 'Mohandas Gandhi',
            'company': 'Gandhi, PC',
            'address': '225 Paper Street, Porbandar, India',
            'phone1': '123.456.7890',
            'phone1_label': 'Work',
            'email': 'gandhi@gandhi.com',
            'website': 'gandhi.com',
            'notes': 'The Mahatma',
        }
        for key, val in expectedValues.items():
            self.assertEqual(getattr(contact, key), val)
        self.assertEqual(str(contact), f'{contact.name} {contact.id}')

    def testContactContentSecond(self):
        contact = Contact.objects.get(id=2)
        self.assertEqual(str(contact), f'{contact.name} {contact.id}')


