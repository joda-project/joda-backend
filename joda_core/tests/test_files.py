import os

from django.test import TestCase

import joda_core.files.utils as utils


class FileUtilsTestCase(TestCase):
    def test_file_properties(self):
        """Test file MD5 and size"""
        sample_pdf = 'sample.pdf'
        os.environ[utils.UPLOADS_KEY] = 'test_data'

        path = utils.upload_path()
        self.assertEqual(path, 'test_data')
        self.assertEqual(utils.get_size(sample_pdf), 7104)
        with open(os.path.join(path, sample_pdf), 'rb') as f:
            self.assertEqual(utils.get_md5(f), '84ccae833dd13ee79642d0095440da9a')

        os.environ[utils.UPLOADS_KEY] = 'jure'
        self.assertEqual(utils.upload_path(), 'test_data')
