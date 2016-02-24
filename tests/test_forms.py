from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.testcases import TestCase

from dbstorage.forms import DBFileForm


class DBFileFormTests(TestCase):

    def test_save(self):
        form = DBFileForm(data={'name': 'hello-world.txt'}, files={
            'file': SimpleUploadedFile('test.file', b'Hello World!'),
        })
        self.assertTrue(form.is_valid(), form.errors)

        db_file = form.save()
        self.assertTrue(db_file.pk)
        self.assertEqual(db_file.size, 12)
        self.assertEqual(db_file.content, b'Hello World!')
        self.assertEqual(db_file.name, 'hello-world.txt')
