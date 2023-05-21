"""Cookie Admin."""
from django.contrib import admin
from django.db import models, transaction

from martor.widgets import AdminMartorWidget

from apps.translations.admin import TranslatableAdmin, TranslationInline
from apps.translations.tasks import translate_object

from .models import AdBlock, Cookie


class CookieAdmin(TranslatableAdmin, admin.ModelAdmin):
    """Cookie Admin."""

    actions = ["make_published", "make_draft"]
    list_display = ("title", "state")
    fields = (
        "title",
        "state",
        "message",
        "essential_functional_cookies_description",
        "analytical_cookies_description",
        "external_content_cookies_description",
    )

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
    inlines = [
        TranslationInline,
    ]

    def save_model(self, request, obj, form, change):
        """Translate empty cookie fields."""
        obj.user = request.user
        transaction.on_commit(lambda: translate_object.delay("cookies.Cookie", obj.id))
        super().save_model(request, obj, form, change)


class AdBlockAdmin(TranslatableAdmin, admin.ModelAdmin):
    """AdBlock Admin."""

    actions = ["make_published", "make_draft"]
    list_display = ("title", "state")
    fields = (
        "title",
        "state",
        "message",
        "button_text",
    )

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
    inlines = [
        TranslationInline,
    ]

    def save_model(self, request, obj, form, change):
        """Translate empty AdBlock fields."""
        obj.user = request.user
        transaction.on_commit(lambda: translate_object.delay("cookies.AdBlock", obj.id))
        super().save_model(request, obj, form, change)


admin.site.register(AdBlock, AdBlockAdmin)


admin.site.register(Cookie, CookieAdmin)
