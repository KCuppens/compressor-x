# Generated by Django 4.1.3 on 2022-11-22 09:23

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Compression",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Unique identification",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date of creation"),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Date of last update"),
                ),
                (
                    "date_deleted",
                    models.DateTimeField(blank=True, null=True, verbose_name="Delete date"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
