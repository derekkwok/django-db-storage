from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone

from dbstorage.models import DBFile

import datetime
import os


class Command (BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', default=False, help='Clears out the db_files table before importing')
        parser.add_argument('--path', default=settings.MEDIA_ROOT, help='The root directory to import into the db_files table')

    def handle(self, *args, **options):
        if options['clear']:
            DBFile.objects.all().delete()
        media_root = os.path.abspath(options['path'])
        for root, dirs, files in os.walk(media_root):
            for f in files:
                if f.startswith('.'):
                    continue
                file_path = os.path.join(root, f)
                rel_path = os.path.relpath(file_path, media_root)
                if DBFile.objects.filter(name=rel_path).exists():
                    print('"%s" already exists in the database, skipping' % rel_path)
                    continue
                mtime = os.path.getmtime(file_path)
                mod_time = timezone.make_aware(datetime.datetime.utcfromtimestamp(mtime), timezone.utc)
                with open(file_path, 'rb') as f:
                    DBFile.objects.create(content=f.read(), name=rel_path, created_on=mod_time, updated_on=mod_time)
