from django.conf.urls import url

from dbstorage.views import DBFileView

urlpatterns = [

    url(r'^media/(?P<name>.*)$', DBFileView.as_view()),

]
