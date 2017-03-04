"""joda module tests"""

import json

from django.test import TestCase
from rest_framework.test import APIClient

import joda.helpers
import joda.version


class HelpersTestCase(TestCase):
    """Helpers test case"""

    def test_features(self):
        """Test features dictionary generation"""
        features = joda.helpers.features()
        self.assertTrue('misc' in features)
        self.assertEqual(features['misc']['module'], 'joda_misc')

    def test_about_view(self):
        """Test about API view"""
        client = APIClient()
        response = json.loads(client.get('/api/about', format='json').content.decode('utf-8'))
        self.assertTrue('data' in response)
        self.assertTrue('features' in response['data'])
        self.assertEqual(response['data']['version'], joda.version.get_version())


class VersionTestCase(TestCase):
    """Version parsing test case"""

    def test_version(self):
        """Test version parsing"""
        with open('VERSION') as version_file:
            version = version_file.read().strip()

        joda.version.get_version()
        self.assertEqual(joda.version.get_version(no_revision=True), version)

    def test_git_changeset(self):
        """Test git changeset parsing"""
        joda.version.get_git_changeset()
        self.assertEqual(joda.version.get_git_changeset('..'), '')
