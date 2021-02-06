from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.urls import reverse

from dbstorage.forms import DBFileForm
from dbstorage.models import DBFile


@admin.register(DBFile)
class DBFileAdmin(admin.ModelAdmin):

    form = DBFileForm
    list_display = ['name', 'download', 'file_size', 'updated_on', 'created_on']
    ordering = ['name']
    search_fields = ['name']

    def download(self, obj):
        href = reverse('db_file', args=[obj.name])
        return '<a href="{}" target="_blank">Download</a>'.format(href)
    download.allow_tags = True
    download.short_description = ''

    def file_size(self, obj):
        return filesizeformat(obj.size)
    file_size.short_description = 'size'

    def get_queryset(self, request):
        qs = super(DBFileAdmin, self).get_queryset(request)
        qs = qs.defer('content')
        return qs
