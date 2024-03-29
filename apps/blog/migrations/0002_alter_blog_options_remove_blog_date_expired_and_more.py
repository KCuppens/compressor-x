# Generated by Django 4.1.3 on 2022-11-18 15:02

from django.db import migrations, models

import django_extensions.db.fields


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blog",
            options={
                "ordering": ["-date_created"],
                "verbose_name": "Blog",
                "verbose_name_plural": "Blog",
            },
        ),
        migrations.RemoveField(
            model_name="blog",
            name="date_expired",
        ),
        migrations.RemoveField(
            model_name="blog",
            name="date_published",
        ),
        migrations.AddField(
            model_name="blog",
            name="markup_data",
            field=models.TextField(blank=True, null=True, verbose_name="Structured markup data"),
        ),
        migrations.AddField(
            model_name="blog",
            name="meta_description",
            field=models.TextField(blank=True, null=True, verbose_name="Meta description"),
        ),
        migrations.AddField(
            model_name="blog",
            name="meta_image",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Meta image"
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="meta_keywords",
            field=models.TextField(
                blank=True, max_length=255, null=True, verbose_name="Meta keywords"
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="meta_title",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=55,
                null=True,
                verbose_name="Meta title",
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                populate_from="name",
                unique=True,
                verbose_name="Slug",
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Date of creation"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="description",
            field=models.TextField(blank=True, verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="image",
            field=models.ImageField(upload_to="blog/", verbose_name="Image"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="keywords",
            field=models.TextField(blank=True, verbose_name="Keywords"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="state",
            field=models.CharField(
                choices=[("draft", "Draft"), ("published", "Published")],
                default="draft",
                max_length=255,
            ),
        ),
    ]
