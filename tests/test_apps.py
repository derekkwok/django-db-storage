from django.test.testcases import TestCase

import dbfiles
from dbfiles.apps import DBFilesConfig


class DBFilesConfigTests(TestCase):
    def test_app_config(self):
        config = DBFilesConfig("dbfiles", dbfiles)
        self.assertEqual(config.verbose_name, "DB Files")
