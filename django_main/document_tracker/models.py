from django.db import models


class File(models.Model):
    file_content = models.FileField(upload_to="uploads/")
    created_date = models.DateTimeField("date created")
    last_modified_date = models.DateTimeField("date last modified")


class Tag(models.Model):
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.title


class FileTag(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
