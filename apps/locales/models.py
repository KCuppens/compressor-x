from django.db import models
from django.utils.translation import gettext_lazy as _

from .tasks import translate_all_objects


class Locale(models.Model):
    """Locale model."""

    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=255)
    deepl_code = models.CharField(max_length=5, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    is_translated = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Locale")
        verbose_name_plural = _("Locales")
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if self.is_default:
            Locale.objects.exclude(pk=self.pk).update(is_default=False)
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            translate_all_objects.delay(self.id)
