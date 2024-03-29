"""This module contains the admins for the Translations app."""

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models

from martor.widgets import AdminMartorWidget

from .forms import generate_translation_form
from .models import Translation


__docformat__ = "restructuredtext"


class TranslatableAdminMixin:
    """An admin mixin which provides custom translation functionalities."""

    def prepare_translation_inlines(self, inlines, inline_type):
        """Prepare the translation inlines of the admin."""
        form = generate_translation_form(self.model)
        remove_inlines = []
        for i, v in enumerate(inlines):
            if isinstance(v, inline_type):
                if len(form.base_fields["field"].choices) == 1:
                    remove_inlines.append(i)
                else:
                    inlines[i].form = form
        remove_inlines.reverse()
        for index in remove_inlines:
            inlines.pop(index)


class TranslatableAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """The admin which represents the `Translatable` instances."""

    def get_inline_instances(self, request, obj=None):
        """Get the inline instances of the admin."""
        inlines = list(super(TranslatableAdmin, self).get_inline_instances(request, obj))
        self.prepare_translation_inlines(inlines, TranslationInline)
        return inlines


class TranslationInline(GenericStackedInline):
    """The inline which represents the `Translation` instances."""

    model = Translation
    extra = 1
    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
