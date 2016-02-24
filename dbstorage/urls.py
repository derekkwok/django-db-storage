import re

from django.conf import settings
from django.conf.urls import url

from dbstorage import views


def dbstorage_url(prefix=settings.MEDIA_URL, view=views.DBFileView.as_view(), name='db_file', **kwargs):
    prefix = re.escape(prefix.lstrip('/'))
    return url(r'^{}(?P<name>.*)$'.format(prefix), view, name=name, kwargs=kwargs)


urlpatterns = [
    dbstorage_url(''),
]
