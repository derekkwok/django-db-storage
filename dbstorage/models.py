from django.db import models


class DBFile(models.Model):

    content = models.BinaryField()
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'db_file'

    def save(self, *args, **kwargs):
        self.size = len(self.content)
        super(DBFile, self).save(*args, **kwargs)
