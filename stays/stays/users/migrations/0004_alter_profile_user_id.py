# Generated by Django 4.2.5 on 2023-10-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_rename_number_of_publications_profile_user_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user_id",
            field=models.IntegerField(default=1),
        ),
    ]
