from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

from dbfiles.models import DBFile
from dbfiles.storage import DBStorage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            default=False,
            help="Deletes orphaned db_file rows, instead of just listing them",
        )

    def handle(self, *args, **options):
        # Grab a set of all known files in the database.
        db_files = set(DBFile.objects.values_list("name", flat=True))
        # Loop through every model we know about, and find any FileField (or ImageField) whose storage is DBStorage.
        # Keep a set of filenames that exist in any model in the system.
        model_files = set()
        for config in apps.get_app_configs():
            for model in config.get_models():
                for field in model._meta.get_fields():
                    if isinstance(field, models.FileField) and issubclass(field.storage.__class__, DBStorage):
                        model_files.update(model.objects.order_by().values_list(field.name, flat=True))
        # Orphans are then just files that exist in db_file but nowhere else in the system.
        orphans = db_files - model_files
        for filename in sorted(orphans):
            if options["clear"]:
                print("Deleting %s" % filename)
                DBFile.objects.filter(name=filename).delete()
            else:
                print(filename)
