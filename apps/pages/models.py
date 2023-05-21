from django.db import models

from django_extensions.db.fields import AutoSlugField

from apps.base.models import BaseModel, SeoModel
from apps.translations.models import Translatable


class Page(BaseModel, SeoModel, Translatable):
    key_name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    class TranslationMeta:
        fields = [
            "title",
            "subtitle",
            "content",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]


class PageElement(BaseModel, Translatable):
    key_name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = AutoSlugField(populate_from="title", unique=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="page_elements", blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.URLField(blank=True, null=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="elements")

    class Meta:
        verbose_name = "Page Element"
        verbose_name_plural = "Page Elements"

    class TranslationMeta:
        fields = ["title", "subtitle", "slug", "content", "button_text", "button_url"]


class PageText(BaseModel, Translatable):
    key_name = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Page Text"
        verbose_name_plural = "Page Texts"

    class TranslationMeta:
        fields = [
            "text",
        ]
