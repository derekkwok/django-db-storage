# django-dbfiles

A fork of [django-db-storage](https://github.com/derekkwok/django-db-storage), updated for modern versions of Django (and renamed for inclusion in PyPI).

## Overview

*Warning*: In many cases, storing files in the database is a BAD idea. Your database will easily become bloated and theperformance can degrade rapidly. See this [StackExchange post](http://programmers.stackexchange.com/questions/150669/is-it-a-bad-practice-to-store-large-files-10-mb-in-a-database) for more information.

This is a custom storage backend for storing files in the database instead of the file system and is a drop-in replacement for Django's FileSystemStorage. Some benefits of this application:

* no changes needed to existing models, it just works (and if it doesn't, open a ticket!)
* django-admin is implemented and can be used to search, upload, download and manage files
* 100% code coverage with unit tests

![Admin List](http://i.imgur.com/4g9tmEZt.png)
![Admin Edit](http://i.imgur.com/A2F8xlrt.png)

## Requirements

* Python (3.5, 3.6, 3.7, 3.8)
* Django (2.2, 3.0, 3.1)

## Installation

Installation using pip:

```
pip install django-dbfiles
```

Update `settings.py`:

```python
# Add 'dbfiles' to INSTALLED_APPS
INSTALLED_APPS = [
    'dbfiles',
]

# Optionally set DEFAULT_FILE_STORAGE
DEFAULT_FILE_STORAGE = 'dbfiles.storage.DBStorage'

# Choose a root url for uploaded files
MEDIA_URL = '/media/'
```

Update `urls.py`:

```python
urlpatterns = [
    ...
    dbfiles_url(),
]
```

Run database migrations:

```
python manage.py migrate
```

## How to Use

No modification are needed for models to work properly.

```python
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class MyModel(models.Model):
    file_field1 = models.FileField()
    file_field2 = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_field3 = models.FileField(upload_to=user_directory_path)
```

## Moving from django-db-storage?

If you are switching to this package from `django-db-storage` and want to keep your existing `db_file` table, let Django know about the app name change by running the following SQL:

```sql
UPDATE django_migrations SET app = 'dbfiles' WHERE app = 'dbstorage';
```

## Bugs?

Create an issue at https://github.com/imsweb/django-dbfiles/issues
