from django.core.validators import MaxValueValidator, MinValueValidator


RESIZE_TYPE_PERCENTAGE = "percentage"
RESIZE_TYPE_PIXELS = "pixel"

RESIZE_TYPES = [
    (RESIZE_TYPE_PIXELS, "Pixels"),
    (RESIZE_TYPE_PERCENTAGE, "Percentage"),
]

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

FILTER_TYPE_NEAREST = "nearest"
FILTER_TYPE_BOX = "box"
FILTER_TYPE_BILINEAR = "bilinear"
FILTER_TYPE_HAMMING = "hamming"
FILTER_TYPE_BICUBIC = "bicubic"
FILTER_TYPE_LANCZOS = "lanczos"

FILTER_TYPES = [
    (FILTER_TYPE_NEAREST, "Nearest"),
    (FILTER_TYPE_BOX, "Box"),
    (FILTER_TYPE_BILINEAR, "Bilinear"),
    (FILTER_TYPE_HAMMING, "Hamming"),
    (FILTER_TYPE_BICUBIC, "Bicubic"),
    (FILTER_TYPE_LANCZOS, "Lanczos"),
]

DEVICE_TYPE_OWN = "own"
DEVICE_TYPE_DESKTOP = "desktop"
DEVICE_TYPE_MOBILE = "mobile"
DEVICE_TYPE_TABLET = "tablet"

DEVICE_TYPES = [
    (DEVICE_TYPE_OWN, "-"),
    (DEVICE_TYPE_DESKTOP, "Desktop"),
    (DEVICE_TYPE_MOBILE, "Mobile"),
    (DEVICE_TYPE_TABLET, "Tablet"),
]

CONVERT_TYPE_DEFAULT = "remain"
CONVERT_TYPE_PNG = "png"
CONVERT_TYPE_WEBP = "webp"
CONVERT_TYPE_JPEG = "jpeg"

CONVERT_TYPES = [
    (CONVERT_TYPE_DEFAULT, "-"),
    (CONVERT_TYPE_PNG, "png"),
    (CONVERT_TYPE_WEBP, "webp"),
    (CONVERT_TYPE_JPEG, "jpeg"),
]

FIT_TYPE_CROP = "crop"
FIT_TYPE_RESIZE = "resize"
FIT_TYPE_SCALE = "resize"

FIT_TYPES = [
    (FIT_TYPE_RESIZE, "Resize"),
    (FIT_TYPE_CROP, "Crop"),
    (FIT_TYPE_SCALE, "Scale"),
]

SUPPORTED_TYPE_JPG = "jpg"
SUPPORTED_TYPE_PNG = "png"
SUPPORTED_TYPE_WEBP = "webp"

SUPPORTED_OPTIONS = [
    (SUPPORTED_TYPE_JPG, "jpg"),
    (SUPPORTED_TYPE_PNG, "png"),
    (SUPPORTED_TYPE_WEBP, "webp"),
]

IMAGE_QUALITY_LOSSLESS = 70
IMAGE_QUALITY_LOSSY = 50
