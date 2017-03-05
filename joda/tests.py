"""joda module tests"""

import json

from django.test import TestCase
from rest_framework.test import APIClient

import joda
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
        self.assertEqual(response['data']['version'], joda.version_string)


class VersionTestCase(TestCase):
    """Version parsing test case"""

    def test_version(self):
        """Test version parsing"""
        self.assertEqual(joda.version.get_version((1, 0, 0, 'alpha', 1)), '1.0.0a1')
        self.assertEqual(joda.version.get_version((1, 0, 0, 'beta', 1)), '1.0.0b1')
        self.assertEqual(joda.version.get_version((1, 0, 0, 'rc', 1)), '1.0.0rc1')
        self.assertEqual(joda.version.get_version((1, 0, 0, 'final', 1)), '1.0.0')


    def test_git_changeset(self):
        """Test git changeset parsing"""
        joda.version.get_git_changeset()
        self.assertEqual(joda.version.get_git_changeset('..'), '')
