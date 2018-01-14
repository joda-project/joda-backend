"""joda_core management commands tests"""

from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from oauth2_provider.models import get_application_model

Application = get_application_model()


class OAuthCreateAppTestCase(TestCase):
    """oauth_create_app test case"""

    def test_command_output(self):
        """Test command output"""
        out = StringIO()
        call_command('oauth_create_app', stdout=out)
        self.assertIn('Successfully created application', out.getvalue())

        exception = False
        try:
            call_command('oauth_create_app')
        except CommandError:
            exception = True
        self.assertTrue(exception)

    def test_command_function(self):
        """Test command function"""

        self.assertEqual(Application.objects.count(), 0)

        out = StringIO()
        call_command('oauth_create_app', stdout=out)

        self.assertEqual(Application.objects.count(), 1)
