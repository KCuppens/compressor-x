from django.db import models


class ConfigManager(models.Manager):
    def get_config(self, key_name: str):
        try:
            return self.get(key_name=key_name).value  # type: ignore
        except self.model.DoesNotExist:
            return ""
