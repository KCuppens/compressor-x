from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.base.constants import STATE_DRAFT, STATE_PUBLISHED


@admin.action(description=_("Publish selected %(verbose_name_plural)s"))
def make_published(modeladmin, request, queryset):
    queryset.update(state=STATE_PUBLISHED)


@admin.action(description=_("Draft selected %(verbose_name_plural)s"))
def make_draft(modeladmin, request, queryset):
    queryset.update(state=STATE_DRAFT)
