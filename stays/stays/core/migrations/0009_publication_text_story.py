# Generated by Django 4.2.5 on 2023-12-23 17:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_alter_publication_author_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="text_story",
            field=models.TextField(
                blank=True, help_text="Write your story.", max_length=170, null=True
            ),
        ),
    ]
