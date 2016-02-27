django-db-storage
=================

.. image:: https://travis-ci.org/derekkwok/django-db-storage.svg?branch=master
    :target: https://travis-ci.org/derekkwok/django-db-storage

.. image:: https://coveralls.io/repos/github/derekkwok/django-db-storage/badge.svg?branch=master 
    :target: https://coveralls.io/github/derekkwok/django-db-storage?branch=master

.. image:: https://badge.fury.io/py/django-db-storage.svg
    :target: https://badge.fury.io/py/django-db-storage

Overview
--------

Warning: In many cases, storing files in the database is a BAD idea. Your database will easily become bloated and the performance can degrade rapidly. See this `StackExchange post`_ for more information.

.. _StackExchange post: http://programmers.stackexchange.com/questions/150669/is-it-a-bad-practice-to-store-large-files-10-mb-in-a-database

This is a custom storage backend for storing files in the database instead of the file system and is a drop-in replacement for Django's FileSystemStorage. Some benefits of this application:

* no changes needed to existing models, it just works (and if it doesn't, open a ticket!)
* django-admin is implemented and can be used to search, upload, download and manage files
* 100% code coverage with unit tests

.. image:: http://i.imgur.com/4g9tmEZt.png
    :target: http://i.imgur.com/4g9tmEZ.png

.. image:: http://i.imgur.com/A2F8xlrt.png
    :target: http://i.imgur.com/A2F8xlr.png

Requirements
------------

* Python (2.7, 3.4, 3.5)
* Django (1.8, 1.9)

Installation
------------

Installation using pip::

    $ pip install django-db-storage

Update ``settings.py``

.. code-block:: python

    # Add 'dbstorage' to INSTALLED_APPS
    INSTALLED_APPS = [
        'dbstorage',
    ]

    # Optionally set DEFAULT_FILE_STORAGE
    DEFAULT_FILE_STORAGE = 'dbstorage.storage.DBStorage'

    # Choose a root url for uploaded files
    MEDIA_URL = '/media/'

Update ``urls.py``

.. code-block:: python

    urlpatterns = [
        ...
        dbstorage_url(),
    ]

Run database migrations

::

    $ python manage.py migrate


How to Use
----------

No modification are needed for models to work properly.

.. code-block:: python

    def user_directory_path(instance, filename):
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    class MyModel(models.Model):

        file_field1 = models.FileField()
        file_field2 = models.FileField(upload_to='uploads/%Y/%m/%d/')
        file_field3 = models.FileField(upload_to=user_directory_path)

Bugs?
-----

Create an issue at https://github.com/derekkwok/django-db-storage/issues
