from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .tasks import translate_all_objects


@admin.action(description=_("Activate selected %(verbose_name_plural)s"))
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description=_("Deactivate selected %(verbose_name_plural)s"))
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description=_("Translate selected %(verbose_name_plural)s"))
def make_translations(modeladmin, request, queryset):
    for locale in queryset:
        translate_all_objects.delay(locale.id)
