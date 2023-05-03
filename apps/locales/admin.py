from django.contrib import admin
from django.db import models

from martor.widgets import AdminMartorWidget

from .models import Locale


class LocaleAdmin(admin.ModelAdmin):
    actions = ["make_active", "make_inactive", "make_translations"]
    list_display = ("name", "code", "is_default", "is_active")

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }


admin.site.register(Locale, LocaleAdmin)
