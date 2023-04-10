from django.db import models

from apps.base.models import BaseModel
from apps.compressed_file.models import CompressedFile
from apps.initial_files.models import InitialFile


class Compression(BaseModel):
    initial_file = models.ForeignKey(InitialFile, blank=True, null=True, on_delete=models.CASCADE)
    compressed_file = models.ForeignKey(
        CompressedFile, blank=True, null=True, on_delete=models.CASCADE
    )
