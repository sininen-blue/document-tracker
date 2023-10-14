from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    file_content = models.FileField(upload_to="uploads/")
    file_name = models.CharField(max_length=100)
    created_date = models.DateTimeField("date created", auto_now_add=True)
    last_modified_date = models.DateTimeField("date last modified", auto_now_add=True)

    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.CASCADE)
    last_modified_by = models.ForeignKey(User, related_name='%(class)s_edited_by', on_delete=models.CASCADE)

    version_number = models.IntegerField(default=0)
    version_notes = models.CharField(max_length=256, default="")


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class FileTag(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
