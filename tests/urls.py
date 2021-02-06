from django.conf.urls import url
from django.contrib import admin

from dbstorage.urls import dbstorage_url

urlpatterns = [

    # admin urls
    url(r'^admin/', admin.site.urls),

    # dbstorage
    dbstorage_url(),
]
