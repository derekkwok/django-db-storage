from datetime import timedelta

from django.conf import settings
from django.core.files.base import ContentFile
from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from dbstorage.models import DBFile
from dbstorage.storage import DBStorage


class DBStorageTests(TestCase):

    storage_class = DBStorage

    def setUp(self):
        self.storage = self.storage_class('/test_media_url/')

    def test_default_base_url(self):
        storage = self.storage_class()
        self.assertEqual(storage.base_url, settings.MEDIA_URL)

    def test_default_base_url_append_slash(self):
        storage = self.storage_class('/test')
        self.assertEqual(storage.base_url, '/test/')

    def test_file_access_options(self):
        self.assertFalse(self.storage.exists('storage_test'))

        f = ContentFile(b'storage contents')
        self.storage.save('storage_test', f)
        self.assertEqual(self.storage.size('storage_test'), 16)
        self.assertNumQueries(1, self.storage.size, 'storage_test')

        f = self.storage.open('storage_test')
        self.assertEqual(f.read(), b'storage contents')

        self.storage.delete('storage_test')
        self.assertFalse(self.storage.exists('storage_test'))

    def test_file_created_time(self):
        name = 'test.file'
        DBFile.objects.create(content=b'custom content', name=name)
        ctime = self.storage.created_time(name)

        self.assertEqual(DBFile.objects.get(name=name).created_on, ctime)
        self.assertLess(timezone.now() - self.storage.created_time(name), timedelta(seconds=1))
        self.assertNumQueries(1, self.storage.created_time, name)

    def test_file_modified_time(self):
        name = 'test.file'
        DBFile.objects.create(content=b'custom content', name=name)
        mtime = self.storage.modified_time(name)

        self.assertEqual(DBFile.objects.get(name=name).updated_on, mtime)
        self.assertLess(timezone.now() - self.storage.modified_time(name), timedelta(seconds=1))
        self.assertNumQueries(1, self.storage.modified_time, name)

    @override_settings(USE_TZ=False)
    def test_file_created_time_tz_disabled(self):
        self.test_file_created_time()

    @override_settings(USE_TZ=False)
    def test_file_modified_time_tz_disabled(self):
        self.test_file_modified_time()

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

    def test_get_valid_url_max_length(self):
        name = 'test' * 100
        valid_name = self.storage.get_valid_name(name)
        self.assertEqual(valid_name, name[:255])

    def test_path_not_implemented(self):
        self.assertRaises(NotImplementedError, self.storage.path, '')

    def test_listdir_not_implemented(self):
        self.assertRaises(NotImplementedError, self.storage.listdir, '')

    def test_accessed_time_not_implemented(self):
        self.assertRaises(NotImplementedError, self.storage.accessed_time, '')
