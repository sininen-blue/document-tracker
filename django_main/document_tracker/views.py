from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import os
from django.utils import timezone

from .models import File, Tag, FileTag


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


@login_required(redirect_field_name="auth", login_url="login/")
def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required(redirect_field_name="auth", login_url="login/")
def index(request):
    current_user = request.user.username
    file_list = File.objects.all()
    tag_list = Tag.objects.all()

    # get queries
    q = request.GET.get("q")
    active_filters = request.GET.getlist("active-filters")
    sort_type = request.GET.get("sort")

    if q != "" and q is not None:
        file_list = file_list.filter(file_name__icontains=q)
    else:
        q = ""
        file_list = file_list.filter(latest=True)

    if active_filters != "" and active_filters is not None:
        q_object = Q()
        for filter in active_filters:
            q_object = Q(tags__tag__title=filter)

        file_list = file_list.filter(q_object)

    if sort_type == "" or sort_type is None:
        sort_type = "file_name"

    file_list = file_list.order_by(sort_type)

    context = {
        "query": q,
        "active_filters": active_filters,
        "sort_type": sort_type,
        "user": current_user,
        "file_list": file_list,
        "tag_list": tag_list,
    }
    return render(request, "document_tracker/index.html", context)


@login_required(redirect_field_name="auth", login_url="login/")
def detail(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, "document_tracker/detail.html", {"file": file})


@login_required(redirect_field_name="auth", login_url="login/")
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
                version_number=previous_version.version_number + 1,
                version_notes=uploaded_version_notes,
            )
        else:
            File.objects.create(
                file_content=uploaded_file,
                file_name=uploaded_file_name,
                created_by=request.user,
                last_modified_by=request.user,
                version_number=1,
                version_notes=uploaded_version_notes,
            )

        return redirect("/")
    else:
        return render(request, "document_tracker/import_file.html")


@login_required(redirect_field_name="auth", login_url="login/")
def export_file(request, file_id):
    file = File.objects.get(pk=file_id)
    response = HttpResponse(
        file.file_content, content_type="application/force-download"
    )
    file_extension = os.path.splitext(file.file_content.name)
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{file.file_name}{file_extension[1]}"'
    return response


def rename_file(request, file_id):
    file = File.objects.get(pk=file_id)

    if request.method == "POST":
        new_file_name = request.POST["rename"]
        existing_file_names = File.objects.filter(latest=True)

        if existing_file_names.filter(file_name__exact=new_file_name).exists():
            # if there is already a file that exists with that name
            context = {
                "file": file,
                "error": "File name already used, please choose different one",
            }
            return render(request, "document_tracker/rename.html", context)
        else:
            past_file_versions = File.objects.exclude(pk=file_id).filter(
                file_name=file.file_name
            )
            for past_file in past_file_versions:
                past_file.file_name = new_file_name
                past_file.save()

            file.file_name = new_file_name
            file.last_modified_date = timezone.now()
            file.save()
            return redirect("/")

    return render(request, "document_tracker/rename.html", {"file": file})


@login_required(redirect_field_name="auth", login_url="login/")
def delete_file(request, file_id):
    file_instance = File.objects.get(pk=file_id)
    file_list = File.objects.filter(file_name=file_instance.file_name)

    for file in file_list:
        file.delete()

    return redirect("/")


@login_required(redirect_field_name="auth", login_url="login/")
def add_tag(request, file_id):
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


@login_required(redirect_field_name="auth", login_url="login/")
def remove_tag(request, file_tag_id):
    file_tag_instance = FileTag.objects.get(pk=file_tag_id)
    file_tag_list = FileTag.objects.filter(tag=file_tag_instance.tag)

    if file_tag_list.count() == 1:
        file_tag_instance.delete()
        lone_tag = Tag.objects.get(title=file_tag_instance.tag.title)
        lone_tag.delete()
    else:
        file_tag_instance.delete()

    return redirect("/")
