from PIL import Image as PillImage

from apps.compressed_file.utils import get_compressed_file_path


class AutoCompress:
    def image_quality_setting(self, action):
        if action.config_file.lossless:
            image_quality = 50
        elif action.config_file.lossy:
            image_quality = 70
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
        return image
