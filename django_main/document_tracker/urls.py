from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("file/<int:file_id>/", views.detail, name="detail"),
]
