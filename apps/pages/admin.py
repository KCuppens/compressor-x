"""Faq admin."""
from django.contrib import admin
from django.db import models, transaction

from martor.widgets import AdminMartorWidget

from apps.translations.admin import TranslatableAdmin, TranslationInline
from apps.translations.tasks import translate_object

from .models import Page, PageElement, PageText


class PageElementAdminInline(admin.TabularInline):
    """Question admin inline."""

    model = PageElement
    extra = 1
    fields = ("title", "subtitle", "content", "image", "button_text", "button_url")


class PageAdmin(TranslatableAdmin, admin.ModelAdmin):
    """Page admin."""

    actions = ["make_published", "make_draft"]
    search_fields = ("key_name",)
    list_display = ("key_name", "title")

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
    inlines = [PageElementAdminInline, TranslationInline]

    def save_model(self, request, obj, form, change):
        """Save the model and auto translate."""
        obj.user = request.user
        transaction.on_commit(lambda: translate_object.delay("pages.Page", obj.id))
        super().save_model(request, obj, form, change)
        for question in obj.elements.all():
            transaction.on_commit(
                lambda: translate_object.delay("pages.PageElement", question.id)  # noqa B023
            )


class PageTextAdmin(TranslatableAdmin, admin.ModelAdmin):
    actions = ["make_published", "make_draft"]
    search_fields = ("key_name",)
    list_display = ("key_name", "text")

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
    inlines = [
        TranslationInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        transaction.on_commit(lambda: translate_object.delay("pages.PageText", obj.id))
        super().save_model(request, obj, form, change)


admin.site.register(Page, PageAdmin)
admin.site.register(PageText, PageTextAdmin)
