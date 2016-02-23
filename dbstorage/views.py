import mimetypes
import time

from django.conf import settings
from django.http.response import FileResponse, HttpResponseNotModified
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.http import http_date
from django.views.generic.base import View
from django.views.static import was_modified_since

from dbstorage.models import DBFile


class DBFileView(View):

    def get(self, request, name):
        db_file = get_object_or_404(DBFile.objects.defer('content'), name=name)

        if settings.USE_TZ:
            assert type(db_file.updated_on.tzinfo) == timezone.UTC

        mtime = time.mktime(db_file.updated_on.timetuple())
        modified = was_modified_since(
            header=self.request.META.get('HTTP_IF_MODIFIED_SINCE'),
            mtime=mtime,
            size=db_file.size)

        if not modified:
            return HttpResponseNotModified()

        content_type, encoding = mimetypes.guess_type(db_file.name)
        content_type = content_type or 'application/octet-stream'

        response = FileResponse(db_file.content, content_type=content_type)
        response['Last-Modified'] = http_date(mtime)
        response['Content-Length'] = db_file.size
        if encoding: response['Content-Encoding'] = encoding
        return response
