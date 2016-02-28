from django.test.testcases import TestCase

import dbstorage
from dbstorage.apps import DBStorageConfig


class DBStorageConfigTests(TestCase):

    def test_app_config(self):
        config = DBStorageConfig('dbstorage', dbstorage)
        self.assertEqual(config.verbose_name, 'DB Storage')
