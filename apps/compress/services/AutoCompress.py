import logging

from PIL import Image as PillImage

from apps.compressed_file.utils import get_compressed_file_path
from apps.config_file.constants import IMAGE_QUALITY_LOSSLESS, IMAGE_QUALITY_LOSSY


logger = logging.getLogger(__name__)


class AutoCompress:
    def image_quality_setting(self, action):
        if action.config_file.custom:
            image_quality = action.config_file.image_quality
        elif action.config_file.lossless:
            image_quality = IMAGE_QUALITY_LOSSLESS
        elif action.config_file.lossy:
            image_quality = IMAGE_QUALITY_LOSSY
        return image_quality

    def optimize_image(self, img, image_quality, initial_file_obj):
        # Optimize image
        data = list(img.getdata())
        image = PillImage.new(img.mode, img.size)
        image.putdata(data)
        image.save(
            get_compressed_file_path(initial_file_obj),
            img.format,
            optimize=True,
            quality=image_quality,
        )
        logger.info(
            f"Image saved to {get_compressed_file_path(initial_file_obj)} with quality"
            f"{image_quality} and filetype {img.format}"
        )
        return image
