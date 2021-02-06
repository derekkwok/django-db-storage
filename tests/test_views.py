from django.conf import settings
from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from dbstorage.models import DBFile


class DBFileViewTests(TestCase):

    def setUp(self):
        super(DBFileViewTests, self).setUp()
        self.name = 'test/hello_world.txt'
        self.db_file = DBFile.objects.create(
            content=b'Hello World!',
            name=self.name)
        self.url = reverse('db_file', args=[self.name])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertEqual(response['Content-Length'], '12')
        self.assertFalse('Content-Encoding' in response)
        self.assertTrue('Last-Modified' in response)

    @override_settings(TIME_ZONE='America/Toronto')
    def test_get_not_utc(self):
        self.assertEqual(settings.TIME_ZONE, 'America/Toronto')
        self.test_get()

    @override_settings(USE_TZ=False)
    def test_get_tz_disabled(self):
        self.assertFalse(settings.USE_TZ)
        self.test_get()

    def test_get_not_modified(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Last-Modified' in response)

        response = self.client.get(
            path='/media/{}'.format(self.name),
            HTTP_IF_MODIFIED_SINCE=response['Last-Modified'])
        self.assertEqual(response.status_code, 304)

    def test_get_modified(self):
        self.db_file.content = b'Updated Content!'
        self.db_file.save()

        response = self.client.get(
            path=self.url,
            HTTP_IF_MODIFIED_SINCE='invalid-last-modified')
        self.assertEqual(response.status_code, 200)

    def test_get_not_modified_bad_string(self):
        response = self.client.get(
            path=self.url,
            HTTP_IF_MODIFIED_SINCE='invalid-last-modified')
        self.assertEqual(response.status_code, 200)
