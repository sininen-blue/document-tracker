# Generated by Django 4.2.6 on 2023-10-14 06:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "document_tracker",
            "0007_file_created_by_file_file_name_file_last_modified_by_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="file_name",
            field=models.CharField(max_length=100),
        ),
    ]
