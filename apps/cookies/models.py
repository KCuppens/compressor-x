"""Cookies models."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel, StateModel
from apps.translations.models import Translatable


class Cookie(BaseModel, StateModel, Translatable):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Title"))
    message = models.TextField(null=True, blank=True, verbose_name=_("Message"))
    essential_functional_cookies_description = models.TextField(
        null=True, blank=True, verbose_name=_("Essential and functional cookie description")
    )
    analytical_cookies_description = models.TextField(
        null=True, blank=True, verbose_name=_("Analytical cookie description")
    )
    external_content_cookies_description = models.TextField(
        null=True, blank=True, verbose_name=_("External content cookie description")
    )

    def __str__(self):
        """Return the title of the cookie."""
        return self.title

    class Meta:
        verbose_name = _("Cookie")
        verbose_name_plural = _("Cookies")
