# Generated by Django 4.1.3 on 2023-05-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="key_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]