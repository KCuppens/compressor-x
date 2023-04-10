from django.db import models

import apps.initial_files.constants as C
from apps.base.models import BaseModel


class CompressedFile(BaseModel):
    file = models.FileField(max_length=255)
    status = models.CharField(max_length=255, choices=C.STATUSES_FILE, default=C.STATUS_OPEN)
