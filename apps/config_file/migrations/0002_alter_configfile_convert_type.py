# Generated by Django 4.1.3 on 2022-11-26 14:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("config_file", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="configfile",
            name="convert_type",
            field=models.CharField(
                choices=[
                    ("remain", "-"),
                    ("png", "png"),
                    ("webp", "webp"),
                    ("jpeg", "jpeg"),
                ],
                default="remain",
                max_length=50,
            ),
        ),
    ]
