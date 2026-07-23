from django.test import TestCase

from accounts.models import User


class AnalyticsDashboardTests(TestCase):
    def test_dashboard_renders_on_empty_database(self):
        user = User.objects.create_user(
            username='smoke', password='smoke-pass-123', role=User.Roles.ADMIN
        )
        self.client.force_login(user)

        response = self.client.get('/analytics/')

        self.assertEqual(response.status_code, 200)
