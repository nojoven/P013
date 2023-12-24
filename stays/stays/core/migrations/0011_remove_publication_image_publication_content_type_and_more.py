# Generated by Django 4.2.5 on 2023-12-23 22:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_remove_publication_author_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="publication",
            name="image",
        ),
        migrations.AddField(
            model_name="publication",
            name="content_type",
            field=models.CharField(
                choices=[("voice", "voice"), ("text", "text")],
                default="text",
                max_length=5,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="publication",
            name="picture",
            field=models.ImageField(
                default="seals-6627197_1280.jpg",
                null=True,
                upload_to="uploads/<django.db.models.fields.CharField>/%Y/%m/%d/<django.db.models.fields.UUIDField>/picture",
            ),
        ),
        migrations.AlterField(
            model_name="publication",
            name="location_of_stay",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="publication",
            name="voice_story",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="uploads/<django.db.models.fields.CharField>/%Y/%m/%d/<django.db.models.fields.UUIDField>/",
            ),
        ),
        migrations.AlterField(
            model_name="publication",
            name="year_of_stay",
            field=models.IntegerField(default=1990, null=True),
        ),
    ]