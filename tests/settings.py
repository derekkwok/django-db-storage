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

MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'dbstorage.storage.DBStorage'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {},
}]

TIME_ZONE = 'UTC'
USE_TZ = True
