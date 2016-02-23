from __future__ import unicode_literals

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'dbstorage',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

ROOT_URLCONF = 'tests.urls'

DEFAULT_FILE_STORAGE = 'dbstorage.storage.DBStorage'
