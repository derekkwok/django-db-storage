from datetime import datetime, timedelta

from django.core.files.base import ContentFile
from django.test.testcases import TestCase

from dbstorage.models import DBFile
from dbstorage.storage import DBStorage


class DBStorageTests(TestCase):

    storage_class = DBStorage

    def setUp(self):
        self.storage = self.storage_class('/test_media_url/')

    def test_file_access_options(self):
        self.assertFalse(self.storage.exists('storage_test'))

        f = ContentFile(b'storage contents')
        self.storage.save('storage_test', f)

        f = self.storage.open('storage_test')
        self.assertEqual(f.read(), b'storage contents')

        self.storage.delete('storage_test')
        self.assertFalse(self.storage.exists('storage_test'))

    def test_file_created_time(self):
        self.assertFalse(self.storage.exists('test.file'))

        f = ContentFile(b'custom contents')
        f_name = self.storage.save('test.file', f)
        ctime = self.storage.created_time(f_name)

        self.assertEqual(DBFile.objects.get(name=f_name).created_on, ctime)
        self.assertLess(datetime.now() - self.storage.created_time(f_name), timedelta(seconds=1))

    def test_file_modified_time(self):
        self.assertFalse(self.storage.exists('test.file'))

        f = ContentFile(b'custom contents')
        f_name = self.storage.save('test.file', f)
        mtime = self.storage.modified_time(f_name)

        self.assertEqual(DBFile.objects.get(name=f_name).updated_on, mtime)
        self.assertLess(datetime.now() - self.storage.modified_time(f_name), timedelta(seconds=1))

    def test_file_save_without_name(self):
        self.assertFalse(self.storage.exists('test.file'))

        f = ContentFile(b'custom contents')
        f.name = 'test.file'

        storage_f_name = self.storage.save(None, f)
        self.assertEqual(storage_f_name, f.name)
        self.assertTrue(DBFile.objects.filter(name=f.name).exists())

    def test_file_url(self):
        self.assertEqual(
            self.storage.url('test.file'),
            '{}{}'.format(self.storage.base_url, 'test.file'))

        self.assertEqual(
            self.storage.url(r"""~!*()'@#$%^&*abc`+ =.file"""),
            """/test_media_url/~!*()'%40%23%24%25%5E%26*abc%60%2B%20%3D.file""")
