from django.urls import path
from . import views

app_name = "document_tracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("file/<int:file_id>/", views.detail, name="detail"),
    path("file/<int:file_id>/add_tag/", views.add_tag, name="add_tag"),
    path("import/", views.import_file, name="import_file"),
    path("export/<int:file_id>/", views.export_file, name="export_file"),
]
# add remove edit delete file
# -add- remove edit delete tag
# add remove edit delete user