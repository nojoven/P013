# Generated by Django 4.2.5 on 2023-12-03 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0015_alter_profile_about_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="profilehasdetecteddata",
            name="connected_profile",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
