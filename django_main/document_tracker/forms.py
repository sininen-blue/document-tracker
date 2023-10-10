from django import forms
from .models import File


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file_content", ]
