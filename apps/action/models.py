from django.db import models

from apps.base.models import BaseModel
from apps.compression.models import Compression
from apps.config_file.models import ConfigFile

from .managers import ActionManager


class Action(BaseModel):
    pass
    # The storage of files in session
    compressions = models.ManyToManyField(Compression, blank=True)

    config_file = models.ForeignKey(ConfigFile, on_delete=models.CASCADE, null=True, blank=True)

    objects = ActionManager()

    def __str__(self):
        return str(self.id)

    def assign_config_file(self):
        """
        Create a new config file and assign it to the action
        """
        self.config_file = ConfigFile.objects.create()

    def save(self, *args, **kwargs):
        self.assign_config_file()
        super().save(*args, **kwargs)
