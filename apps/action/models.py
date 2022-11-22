from django.db import models

from apps.action.managers import ActionManager
from apps.base.models import Base
from apps.compress.models import Compress
from apps.config_file.models import ConfigFile


class Action(Base):
    pass
    # The storage of files in session
    # compresses = models.ForeignKey(Compress, on_delete=models.CASCADE)

    # config_file = models.ForeignKey(ConfigFile, on_delete=models.CASCADE)

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
