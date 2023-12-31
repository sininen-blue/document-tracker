from django.urls import path
from . import views

app_name = "document_tracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("file/<int:file_id>/", views.detail, name="detail"),

    path("file/<int:file_id>/add_tag/", views.add_tag, name="add_tag"),
    path("file/<int:file_tag_id>/remove_tag", views.remove_tag, name="remove_tag"),

    path("file/import", views.import_file, name="import_file"),
    path("file/<int:file_id>/rename", views.rename_file, name="rename_file"),
    path("file/<int:file_id>/export", views.export_file, name="export_file"),
    path("file/<int:file_id>/delete", views.delete_file, name="delete_file"),

    path("login/", views.auth, name="auth"),
    path("logout/", views.logout_view, name="logout_view"),
    path("register/", views.register, name="register"),
]
# add remove edit delete file
# -add- remove edit delete tag
# add remove edit delete user
