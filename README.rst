django-db-storage
=================

.. image:: https://travis-ci.org/derekkwok/django-db-storage.svg?branch=master
    :target: https://travis-ci.org/derekkwok/django-db-storage

.. image:: https://coveralls.io/repos/github/derekkwok/django-db-storage/badge.svg?branch=master 
    :target: https://coveralls.io/github/derekkwok/django-db-storage?branch=master

Overview
--------

Warning: In many cases, storing files in the database is a BAD idea. Your database will easily become bloated and the performance can degrade rapidly. See this `StackExchange post`_ for more information.

.. _StackExchange post: http://programmers.stackexchange.com/questions/150669/is-it-a-bad-practice-to-store-large-files-10-mb-in-a-database

This is a custom storage backend for storing files in the database instead of the file system. It is a drop-in replacement for Django's FileSystemStorage.

Requirements
------------

* Python (2.7, 3.4, 3.5)
* Django (1.8, 1.9)

Installation
------------

Installation using pip::

    $ pip install git+git://github.com/derekkwok/django-db-storage.git

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
