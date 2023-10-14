from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import os

from .forms import UploadFileForm
from .models import File, Tag, FileTag


# TODO tag clean ups, currently when you delete the last instance of a tag,
# it's still a tag
# TODO tag editing, future me problem
# TODO filenames


def auth(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "document_tracker/login.html")
    else:
        return render(request, "document_tracker/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password-confirm"]
        # if user already exists don't allow
        # don't allow empty strings
        # all the other errors too
        if password == password_confirm:
            User.objects.create_user(username, None, password)
            return redirect("/login/")
    else:
        return render(request, "document_tracker/register.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")


def index(request):
    if request.user.is_authenticated:
        file_list = File.objects.filter(latest=True).order_by("file_name")
        file_tag_list = FileTag.objects.all()
        context = {
            "file_list": file_list,
            "file_tag_list": file_tag_list,
        }
        return render(request, "document_tracker/index.html", context)
    else:
        return render(request, "document_tracker/login.html")


def detail(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, "document_tracker/detail.html", {"file": file})


def import_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES["uploaded_file"]
        uploaded_file_name = request.POST["file_name"]
        uploaded_version_notes = request.POST["version_notes"]

        previous_version = File.objects.filter(file_name=uploaded_file_name)
        if previous_version:
            previous_version = previous_version.get(latest=True)
            previous_version.latest = False
            previous_version.save()
            File.objects.create(
                file_content=uploaded_file,
                file_name=uploaded_file_name,
                created_by=previous_version.created_by,
                last_modified_by=request.user,
                version_number=previous_version.version_number+1,
                version_notes=uploaded_version_notes
            )
        else:
            File.objects.create(
                file_content=uploaded_file,
                file_name=uploaded_file_name,
                created_by=request.user,
                last_modified_by=request.user,
                version_number=1,
                version_notes=uploaded_version_notes
            )
        return redirect("/")
    else:
        return render(request, "document_tracker/import_file.html")


def export_file(request, file_id):
    file = File.objects.get(pk=file_id)
    response = HttpResponse(
        file.file_content, content_type="application/force-download"
    )
    response["Content-Disposition"] = f'attachment; filename="{file.file_content}"'
    return response


def delete_file(request, file_id):
    file_instance = File.objects.get(pk=file_id)
    # print(file_instance.file_content)
    os.remove(str(file_instance.file_content))
    File.objects.filter(pk=file_id).delete()
    return redirect("/")


def add_tag(request, file_id):
    # TODO disallow empty tag_names
    file = get_object_or_404(File, pk=file_id)

    found_tag = False
    for tag in Tag.objects.all():
        if tag.title == request.POST["tag_name"]:
            FileTag.objects.create(file=file, tag=tag)
            found_tag = True
            break

    if found_tag is False:
        new_tag = Tag.objects.create(title=request.POST["tag_name"])
        FileTag.objects.create(file=file, tag=new_tag)

    return redirect("/")


def remove_tag(request, file_tag_id):
    FileTag.objects.get(pk=file_tag_id).delete()
    return redirect("/")
