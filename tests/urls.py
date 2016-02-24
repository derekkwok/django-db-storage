from django.conf.urls import url, include
from django.contrib import admin

from dbstorage.urls import dbstorage_url

urlpatterns = [

    # admin urls
    url(r'^admin/', include(admin.site.urls)),

    # dbstorage
    dbstorage_url(),
]
