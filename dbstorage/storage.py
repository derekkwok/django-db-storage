from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.encoding import filepath_to_uri
from django.utils.six.moves.urllib.parse import urljoin

from dbstorage.models import DBFile


class DBStorage(Storage):

    def __init__(self, base_url=None):
        if base_url is None:
            base_url = settings.MEDIA_URL
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url

    def open(self, name, mode='rb'):
        return self._open(name, mode)

    def _open(self, name, mode='rb'):
        f = DBFile.objects.only('content').get(name=name)
        return ContentFile(f.content)

    def _save(self, name, content):
        name = self.get_available_name(name, max_length=255)
        DBFile.objects.create(content=content.read(), name=name)
        return name

    def get_valid_name(self, name):
        return name[:255]

    def path(self, name):
        raise NotImplementedError('DBStorage does not support path() method')

    def delete(self, name):
        DBFile.objects.filter(name=name).delete()

    def exists(self, name):
        return DBFile.objects.filter(name=name).exists()

    def listdir(self, path):
        raise NotImplementedError('DBStorage does not support listdir() method')

    def size(self, name):
        return DBFile.objects.only('size').get(name=name).size

    def url(self, name):
        return urljoin(self.base_url, filepath_to_uri(name))

    def accessed_time(self, name):
        raise NotImplementedError('DBStorage does not support accessed_time() method')

    def created_time(self, name):
        return DBFile.objects.only('created_on').get(name=name).created_on

    def modified_time(self, name):
        return DBFile.objects.only('updated_on').get(name=name).updated_on
