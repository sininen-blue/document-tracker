from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import File, Tag, FileTag


def index(request):
    file_list = File.objects.order_by("-created_date")
    file_tag_list = FileTag.objects.all()
    context = {
        "file_list": file_list,
        "file_tag_list": file_tag_list,
    }
    return render(request, "document_tracker/index.html", context)


def detail(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    
    return render(request, "document_tracker/detail.html", {"file": file})


def add_tag(request, file_id):
    # TODO error handling
    # TODO http response
    
    file = get_object_or_404(File, pk=file_id)
    Tag.objects.create(file=file, title=request.POST["tag_name"], color=request.POST["tag_color"])

    return HttpResponseRedirect("/")
