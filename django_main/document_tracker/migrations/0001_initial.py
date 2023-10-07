# Generated by Django 4.2.6 on 2023-10-07 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_content', models.FileField(upload_to='uploads/')),
                ('created_date', models.DateTimeField(verbose_name='date created')),
                ('last_modified_date', models.DateTimeField(verbose_name='date last modified')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=7)),
            ],
        ),
    ]
