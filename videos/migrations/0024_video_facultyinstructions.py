# Generated by Django 4.0.5 on 2022-10-22 07:41

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0023_video_facultycheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='facultyInstructions',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
