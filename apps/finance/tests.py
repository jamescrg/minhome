
from pprint import pprint

from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser

class ViewTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

    def testCrypto(self):
        response = self.client.get('/crypto/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'crypto')
        self.assertEqual(response.context['crypto_data'][0]['max_supply'], 21000000)
        self.assertTemplateUsed(response, 'crypto/content.html')
        self.assertContains(response, 'BTC')
        self.assertContains(response, 'Bitcoin')
        self.assertContains(response, '24h % Chg')

    def testSecurities(self):
        response = self.client.get('/securities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'securities')
        self.assertIs(response.context['assets'][0]['symbol'], 'GME')
        self.assertGreater(response.context['assets'][0]['price'], 0)
