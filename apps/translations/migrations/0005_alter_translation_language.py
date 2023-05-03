# Generated by Django 4.1.3 on 2023-01-29 08:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("translations", "0004_alter_translation_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="translation",
            name="language",
            field=models.CharField(
                choices=[],
                help_text="the language of the translation",
                max_length=32,
                verbose_name="language",
            ),
        ),
    ]
