from django.test.testcases import TestCase

import dbstorage
from dbstorage.apps import DbstorageConfig


class DbstorageConfigTests(TestCase):

    def test_app_config(self):
        DbstorageConfig('dbstorage', dbstorage)
