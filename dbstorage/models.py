from django.db import models
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class DBFile(models.Model):

    content = models.BinaryField(editable=False)
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'db_file'
        verbose_name = 'DB file'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.size = len(self.content)
        super(DBFile, self).save(*args, **kwargs)
