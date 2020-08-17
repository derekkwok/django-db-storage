from django.contrib import admin
from django.urls import path

from dbfiles.urls import dbfiles_url

urlpatterns = [
    # admin urls
    path("admin/", admin.site.urls),
    # dbfiles
    dbfiles_url(),
]
