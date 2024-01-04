# Generated by Django 4.2.4 on 2024-01-01 00:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0023_delete_guess_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PublicationUpvote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("upvote_date", models.DateTimeField(auto_now_add=True)),
                (
                    "upvote_value",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(
                                0, message="Number of attempts cannot be negative."
                            ),
                            django.core.validators.MaxValueValidator(
                                1,
                                message="Number of attempts cannot exceed the maximum allowed.",
                            ),
                        ],
                    ),
                ),
                (
                    "publication",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.publication",
                    ),
                ),
                (
                    "upvote_profile",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PublicationHasVoter",
        ),
        migrations.AddField(
            model_name="gallery",
            name="is_visible",
            field=models.BooleanField(default=True),
        ),
    ]