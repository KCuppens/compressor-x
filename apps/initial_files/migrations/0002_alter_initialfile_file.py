# Generated by Django 4.1.3 on 2022-11-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("initial_files", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="initialfile",
            name="file",
            field=models.FileField(max_length=255, upload_to=""),
        ),
    ]
