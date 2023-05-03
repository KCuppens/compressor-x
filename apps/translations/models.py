"""This module contains the models for the Translations app."""

import uuid

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .querysets import TranslatableQuerySet
from .utils import get_languages


__docformat__ = "restructuredtext"


class Translation(models.Model):
    """The model which represents the translations."""

    content_type = models.ForeignKey(
        verbose_name=_("content type"),
        help_text=_("the content type of the object to translate"),
        to=ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_("object id"),
        help_text=_("the id of the object to translate"),
        max_length=256,
    )
    field = models.CharField(
        verbose_name=_("field"),
        help_text=_("the field of the object to translate"),
        max_length=64,
    )
    language = models.CharField(
        verbose_name=_("language"),
        help_text=_("the language of the translation"),
        max_length=32,
        choices=get_languages(),
    )
    text = models.TextField(
        verbose_name=_("text"),
        help_text=_("the text of the translation"),
    )

    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id",
    )
    content_type = models.ForeignKey(
        verbose_name=_("content type"),
        help_text=_("the content type of the object to translate"),
        to=ContentType,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Return the representation of the translation."""
        return "{source}: {translation}".format(
            source=getattr(self.content_object, self.field),
            translation=self.text,
        )


class Translatable(models.Model):
    """An abstract model which provides custom translation functionalities."""

    class Meta:
        """The meta data of the `Translatable` model."""

        abstract = True

    class TranslatableMeta:
        """The meta data of the `Translatable` model."""

        fields = None

    objects = TranslatableQuerySet.as_manager()
    translations = GenericRelation(
        Translation,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="%(app_label)s_%(class)s",
    )

    @classmethod
    def get_translatable_fields(cls):
        """Return the model’s translatable fields."""
        if not hasattr(cls, "_cached_translatable_fields"):
            if cls.TranslatableMeta.fields is None:
                fields = []
                for field in cls._meta.get_fields():
                    if (
                        isinstance(
                            field,
                            (
                                models.CharField,
                                models.TextField,
                            ),
                        )
                        and not isinstance(field, models.EmailField)
                        and not (hasattr(field, "choices") and field.choices)
                    ):
                        fields.append(field)
            else:
                fields = [
                    cls._meta.get_field(field_name) for field_name in cls.TranslatableMeta.fields
                ]
            cls._cached_translatable_fields = fields
        return cls._cached_translatable_fields

    @classmethod
    def _get_translatable_fields_names(cls):
        """Return the names of the model's translatable fields."""
        if not hasattr(cls, "_cached_translatable_fields_names"):
            cls._cached_translatable_fields_names = [
                field.name for field in cls.get_translatable_fields()
            ]
        return cls._cached_translatable_fields_names

    @classmethod
    def _get_translatable_fields_choices(cls):
        """Return the choices of the model's translatable fields."""
        choices = [
            (None, "---------"),
        ]

        for field in cls.get_translatable_fields():
            choice = (field.name, field.verbose_name.title())
            choices.append(choice)

        return choices
