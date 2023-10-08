# Generated by Django 4.2.6 on 2023-10-08 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document_tracker', '0003_tag_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='file',
        ),
        migrations.CreateModel(
            name='FileTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document_tracker.file')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document_tracker.tag')),
            ],
        ),
    ]
