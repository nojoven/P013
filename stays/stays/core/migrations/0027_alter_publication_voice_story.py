# Generated by Django 4.2.4 on 2024-01-04 21:29

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0026_alter_publication_voice_story"),
    ]

    operations = [
        migrations.AlterField(
            model_name="publication",
            name="voice_story",
            field=models.FileField(
                blank=True,
                default=None,
                help_text="Record your story.",
                upload_to=core.models.voice_story_upload_to,
            ),
        ),
    ]
