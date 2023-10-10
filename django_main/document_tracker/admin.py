from django.contrib import admin
from .models import File, Tag, FileTag


admin.site.register(File)
admin.site.register(Tag)
admin.site.register(FileTag)
