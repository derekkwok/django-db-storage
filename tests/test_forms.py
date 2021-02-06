from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.testcases import TestCase

from dbstorage.forms import DBFileForm, DBFileWidget
from dbstorage.models import DBFile


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

    def test_save_with_instance(self):
        content = b'Hello World!'
        name = 'my-files/hello-world.txt'

        db_file = DBFile.objects.create(content=content, name=name)
        form = DBFileForm(instance=db_file, data={
            'name': 'my-files/renamed.txt',
        })
        self.assertTrue(form.is_valid())

        new_db_file = form.save()
        self.assertEqual(db_file.pk, new_db_file.pk)
        self.assertEqual(db_file.content, new_db_file.content)
        self.assertEqual('my-files/renamed.txt', new_db_file.name)

    def test_db_file_widget(self):
        widget = DBFileWidget()
        widget.instance = None
        html = widget.render('file', '')
        self.assertTrue('type="file"' in html)
        self.assertTrue('name="file"' in html)

    def test_db_file_widget_with_instance(self):
        content = b'Hello World!'
        name = 'my-files/hello-world.txt'
        db_file = DBFile.objects.create(content=content, name=name)

        widget = DBFileWidget()
        widget.instance = db_file
        html = widget.render('file', '')
        self.assertTrue('<table>' in html)
