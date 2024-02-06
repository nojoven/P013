# Generated by Django 4.2.4 on 2024-02-05 23:32

import core.utils.models_helpers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "__first__"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_online",
                    models.BooleanField(default=False, verbose_name="Online Status"),
                ),
                (
                    "slug",
                    models.SlugField(
                        default=None, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=users.utils.uuid_generator, editable=False, null=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Your email address",
                        max_length=100,
                        null=True,
                        unique=True,
                    ),
                ),
                ("username", models.CharField(max_length=44, null=True, unique=True)),
                (
                    "password",
                    models.CharField(
                        help_text="Your password", max_length=255, null=True
                    ),
                ),
                (
                    "year_of_birth",
                    models.IntegerField(default=1900, help_text="User's birth year"),
                ),
                ("season_of_birth", models.CharField(default="Spring", max_length=50)),
                ("first_name", models.CharField(max_length=25, null=True)),
                ("last_name", models.CharField(max_length=35, null=True)),
                (
                    "motto",
                    models.CharField(default="I LOVE THIS WEBSITE!", max_length=100),
                ),
                ("signature", models.CharField(max_length=150, null=True, unique=True)),
                (
                    "about_text",
                    models.TextField(default="Once upon a time...", null=True),
                ),
                (
                    "continent_of_birth",
                    models.CharField(
                        choices=[
                            ("OC", "Oceania"),
                            ("EU", "Europe"),
                            ("AF", "Africa"),
                            ("NA", "North America"),
                            ("AN", "Antarctica"),
                            ("SA", "South America"),
                            ("AS", "Asia"),
                        ],
                        default="AN",
                        max_length=15,
                        null=True,
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        default="blank-profile-picture.jpg",
                        null=True,
                        upload_to=users.utils.profile_picture_upload_to,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProfileHasPublication",
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
                (
                    "publication_of_user",
                    core.utils.models_helpers.UUIDFieldForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.publication",
                    ),
                ),
                (
                    "user_profile",
                    core.utils.models_helpers.SlugFieldForeignKey(
                        blank=True,
                        max_length=255,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        to_field="slug",
                    ),
                ),
            ],
            options={
                "unique_together": {("user_profile", "publication_of_user")},
            },
        ),
    ]
