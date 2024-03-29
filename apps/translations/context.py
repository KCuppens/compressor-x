"""This module contains the context managers for the Translations app."""

from django.db import models

import apps.translations.models  # noqa: F401

from .languages import _get_default_language, _get_translate_language
from .utils import _get_purview, _get_relations_hierarchy, _get_translations


__docformat__ = "restructuredtext"


class Context:
    """A context manager which provides custom translation functionalities."""

    def __init__(self, entity, *relations):
        """Initialize a `Context` with an entity and some relations of it."""
        hierarchy = _get_relations_hierarchy(*relations)
        self.mapping, self.query = _get_purview(entity, hierarchy)

    def delete(self, lang=None):
        r"""Delete the translations of the `Context`\ 's `purview` in a language."""
        lang = _get_translate_language(lang)
        if lang != _get_default_language():
            _get_translations(self.query, lang).delete()

    def create(self, lang=None):
        r"""
        Create the translations of the `Context`\ 's `purview` in a language.
        """
        language = _get_translate_language(lang)
        if language != _get_default_language():
            _translations = [
                apps.translations.models.Translation(language=language, text=text, **address)
                for address, text in self._get_changed_fields()
            ]
            apps.translations.models.Translation.objects.bulk_create(_translations)

    def read(self, lang=None):
        r"""Read the translations of the `Context`\ 's `purview` in a language."""
        lang = _get_translate_language(lang)
        if lang != _get_default_language():
            _translations = _get_translations(self.query, lang)
            for translation in _translations:
                ct_id = translation.content_type.id
                obj_id = translation.object_id
                field = translation.field
                text = translation.text
                obj = self.mapping[ct_id][obj_id]
                if field in type(obj)._get_translatable_fields_names():
                    setattr(obj, field, text)
        else:
            self.reset()

    def update(self, lang=None):
        r"""Update the translations of the `Context`\ 's `purview` in a language."""
        lang = _get_translate_language(lang)
        if lang != _get_default_language():
            query = models.Q()
            _translations = []
            for address, text in self._get_changed_fields():
                query |= models.Q(**address)
                _translations.append(
                    apps.translations.models.Translation(language=lang, text=text, **address)
                )
            _get_translations(query, lang).delete()
            apps.translations.models.Translation.objects.bulk_create(_translations)

    def reset(self):
        r"""
        Reset translations.

        Reset the translations of the `Context`\ 's `purview` to
        the `default language`.
        """
        for _ct_id, objs in self.mapping.items():  # noqa: F841
            for _obj_id, obj in objs.items():  # noqa: F841
                for field, value in obj._default_translatable_fields.items():
                    setattr(obj, field, value)

    def _get_changed_fields(self):
        r"""Yield the info about the changed fields in the `Context`\ 's `purview`."""
        for ct_id, objs in self.mapping.items():
            for obj_id, obj in objs.items():
                for field in type(obj)._get_translatable_fields_names():
                    text = getattr(obj, field, None)
                    default = obj._default_translatable_fields.get(field, None)
                    if text and text != default:
                        yield (
                            {
                                "content_type_id": ct_id,
                                "object_id": obj_id,
                                "field": field,
                            },
                            text,
                        )

    def __enter__(self):
        """Enter the `Context`."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the `Context`."""
        pass
