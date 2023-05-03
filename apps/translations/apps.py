"""Translations app config."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TranslationsConfig(AppConfig):
    """Translations app config."""

    name = "apps.translations"
    verbose_name = _("Translations")

    def ready(self):
        """Override this to put in."""
        try:
            # cache all content types at the start
            from django.contrib.contenttypes.models import ContentType

            models = [ct.model_class() for ct in ContentType.objects.all()]
            ContentType.objects.get_for_models(*models)
        except Exception:
            pass
