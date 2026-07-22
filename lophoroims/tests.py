from django.test import SimpleTestCase
from django.urls import reverse


class RootRouteTests(SimpleTestCase):
    def test_root_redirects_to_login(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/')
