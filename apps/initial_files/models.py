from django.db import models

from apps.base.models import BaseModel

from .constants import STATUS_OPEN, STATUSES_FILE


class InitialFile(BaseModel):
    file = models.FileField(upload_to="", max_length=255)
    status = models.CharField(max_length=255, choices=STATUSES_FILE, default=STATUS_OPEN)

    def __str__(self):
        return str(self.file)
