# Generated by Django 4.1.3 on 2022-11-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compression", "0001_initial"),
        ("action", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="action",
            name="compressions",
        ),
        migrations.AddField(
            model_name="action",
            name="compressions",
            field=models.ManyToManyField(blank=True, null=True, to="compression.compression"),
        ),
    ]
