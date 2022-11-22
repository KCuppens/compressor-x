from apps.base.models import BaseModel


# from django.db import models
# from apps.initial_file.models import InitialFile
# from apps.compressed_file.models import CompressedFile


class Compression(BaseModel):
    pass
    # initial_file = models.ForeignKey(InitialFile, blank=True, on_delete=models.CASCADE)
    # compressed_file = models.ForeignKey(CompressedFile, blank=True, on_delete=models.CASCADE)
