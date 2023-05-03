"""This module contains the form utilities for the Translations app."""

from django import forms

from .languages import _get_translation_choices
from .models import Translation


__docformat__ = "restructuredtext"


def generate_translation_form(translatable):
    """
    Generate translation form.

    Return the `Translation` form based on a `Translatable` model and
    the `translation language's.
    """
    fields = translatable._get_translatable_fields_choices()
    languages = _get_translation_choices()

    class TranslationForm(forms.ModelForm):
        """The `Translation` form."""

        class Meta:
            """The `Translation` form meta data."""

            model = Translation
            fields = (
                "field",
                "language",
                "text",
            )

        field = forms.ChoiceField(choices=fields)
        language = forms.ChoiceField(choices=languages)

    return TranslationForm
