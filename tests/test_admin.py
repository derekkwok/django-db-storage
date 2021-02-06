from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse

from dbstorage.models import DBFile


class DBFileAdminTests(TestCase):

    def setUp(self):
        super(DBFileAdminTests, self).setUp()
        self.name = 'test/hello_world.txt'
        self.db_file = DBFile.objects.create(
            content=b'Hello World!',
            name=self.name)
        self.url_parts = {
            'app_label': self.db_file._meta.app_label,
            'model_name': self.db_file._meta.model_name,
        }

        User.objects.create_superuser('superuser', '', 'password')
        logged_in = self.client.login(username='superuser', password='password')
        self.assertTrue(logged_in)

    def test_admin_list_view(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(**self.url_parts))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_details_view(self):
        url = reverse('admin:{app_label}_{model_name}_change'.format(**self.url_parts), args=[self.db_file.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
