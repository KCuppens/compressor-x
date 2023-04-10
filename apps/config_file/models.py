from decimal import Decimal

from django.db import models

from apps.base.models import BaseModel

from .constants import (
    CONVERT_TYPE_DEFAULT,
    CONVERT_TYPES,
    DEVICE_TYPE_DESKTOP,
    DEVICE_TYPES,
    FILTER_TYPE_LANCZOS,
    FILTER_TYPES,
    FIT_TYPE_RESIZE,
    FIT_TYPES,
    PERCENTAGE_VALIDATOR,
    RESIZE_TYPE_PERCENTAGE,
    RESIZE_TYPES,
)


class ConfigFile(BaseModel):
    # Resizing options
    resize_type = models.CharField(
        max_length=50, choices=RESIZE_TYPES, default=RESIZE_TYPE_PERCENTAGE
    )
    resize_percentage = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        default=Decimal(0),
        validators=PERCENTAGE_VALIDATOR,
    )
    resize_width = models.IntegerField(default=0)
    resize_height = models.IntegerField(default=0)
    resize_fit = models.CharField(max_length=50, choices=FIT_TYPES, default=FIT_TYPE_RESIZE)
    # Naming options
    rename_prefix = models.CharField(max_length=255, null=True, blank=True)
    rename_suffix = models.CharField(max_length=255, null=True, blank=True)
    # Image options
    keep_exif = models.BooleanField(default=False)
    fix_orientation = models.BooleanField(default=False)
    # Quality options
    image_quality = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        default=Decimal(80),
        validators=PERCENTAGE_VALIDATOR,
    )
    # Selectable options
    custom = models.BooleanField(default=False)
    lossless = models.BooleanField(default=True)
    lossy = models.BooleanField(default=False)
    smallest = models.BooleanField(default=False)
    # Method options
    compression_filter = models.CharField(
        max_length=50, choices=FILTER_TYPES, default=FILTER_TYPE_LANCZOS
    )
    keep_size = models.BooleanField(default=False)
    device_type = models.CharField(
        max_length=25, choices=DEVICE_TYPES, default=DEVICE_TYPE_DESKTOP
    )
    maximum_file_size = models.IntegerField(default=0)
    convert_type = models.CharField(
        max_length=50, choices=CONVERT_TYPES, default=CONVERT_TYPE_DEFAULT
    )
    full_optimized_web_package = models.BooleanField(default=False)
