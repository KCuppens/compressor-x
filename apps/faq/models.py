"""Faq models."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField

from apps.base.models import BaseModel, SeoModel, SortableModel, StateModel
from apps.translations.models import Translatable


class Topic(BaseModel, StateModel, SeoModel, Translatable, SortableModel):
    """Topic model."""

    class Meta:
        """Meta class for Topic."""

        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ["position"]

    class TranslatableMeta:
        """Meta class for Topic translations."""

        fields = ["name", "description", "slug", "meta_title", "meta_description", "meta_keywords"]

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    slug = AutoSlugField(populate_from="name", unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to="service/", null=True, blank=True, verbose_name=_("Image"))

    def __str__(self):
        """Return the name of the topic."""
        return self.name


class Question(BaseModel, StateModel, SeoModel, Translatable, SortableModel):
    """Question model."""

    class Meta:
        """Meta class for Question."""

        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["position"]

    class TranslatableMeta:
        """Meta class for Question translations."""

        fields = ["question", "answer", "meta_title", "meta_description", "meta_keywords"]

    question = models.CharField(max_length=255, verbose_name=_("Question"))
    answer = models.TextField(blank=True, verbose_name=_("Answer"))
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        """Return the question of the question."""
        return self.question
