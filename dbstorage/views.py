import datetime
import mimetypes
import re
from email.utils import format_datetime, parsedate_to_datetime

from django.conf import settings
from django.http.response import FileResponse, HttpResponseNotModified
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.base import View

from dbstorage.models import DBFile


class DBFileView(View):

    def was_modified_since(self, updated_on):
        header = self.request.META.get('HTTP_IF_MODIFIED_SINCE')
        if not header:
            return True
        try:
            matches = re.match(r'^([^;]+)$', header, re.IGNORECASE)
            header_updated_on = parsedate_to_datetime(matches.group(1))
            return updated_on > header_updated_on
        except (AttributeError, ValueError, OverflowError, TypeError):
            return True

    def get(self, request, name):
        db_file = get_object_or_404(DBFile.objects.defer('content'), name=name)

        if settings.USE_TZ:
            assert type(db_file.updated_on.tzinfo) == timezone.UTC
        updated_on = db_file.updated_on.replace(microsecond=0, tzinfo=datetime.timezone.utc)

        if not self.was_modified_since(updated_on):
            return HttpResponseNotModified()

        content_type, encoding = mimetypes.guess_type(db_file.name)
        content_type = content_type or 'application/octet-stream'

        response = FileResponse(db_file.content, content_type=content_type)
        response['Last-Modified'] = format_datetime(updated_on, usegmt=True)
        response['Content-Length'] = db_file.size
        if encoding: response['Content-Encoding'] = encoding
        return response
