# Generated by Django 4.2.5 on 2023-12-25 20:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_alter_publication_location_of_stay"),
    ]

    operations = [
        migrations.RenameField(
            model_name="publication",
            old_name="location_of_stay",
            new_name="country_code_of_stay",
        ),
        migrations.RemoveField(
            model_name="publication",
            name="location_flag_url",
        ),
        migrations.RemoveField(
            model_name="publication",
            name="location_map_url",
        ),
        migrations.RemoveField(
            model_name="publication",
            name="website_ranking",
        ),
        migrations.AddField(
            model_name="publication",
            name="season_of_stay",
            field=models.CharField(
                help_text="Title of your publication.", max_length=70, null=True
            ),
        ),
    ]