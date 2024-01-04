# Generated by Django 4.2.4 on 2024-01-01 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0024_publicationupvote_delete_publicationhasvoter_and_more"),
        ("users", "0031_delete_profilehasdetecteddata"),
    ]

    operations = [
        migrations.AddField(
            model_name="profilehaspublication",
            name="publication_of_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.publication",
            ),
        ),
        migrations.AddField(
            model_name="profilehaspublication",
            name="user_profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="profilehasfollower",
            name="profile_username",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="profilehaspublication",
            unique_together={("user_profile", "publication_of_user")},
        ),
    ]