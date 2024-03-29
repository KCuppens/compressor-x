import logging
import os
from zipfile import ZipFile

from PIL import ExifTags, Image

import apps.config_file.constants as C
from apps.config_file.constants import CONVERT_TYPE_JPEG

from ..utils import get_filename


logger = logging.getLogger(__name__)


class CustomCompress:
    def customize_size(self, config_file):
        device_type = config_file.device_type
        override = False
        if config_file.resize_height and config_file.resize_width:
            height = config_file.resize_height
            width = config_file.resize_width
        elif device_type == C.DEVICE_TYPE_DESKTOP:
            height = 0
            width = 1920
            override = True
        elif device_type == C.DEVICE_TYPE_TABLET:
            height = 0
            width = 650
            override = True
        elif device_type == C.DEVICE_TYPE_MOBILE:
            height = 0
            width = 345
            override = True
        else:
            height = config_file.resize_height
            width = config_file.resize_width
        return height, width, override

    def get_compression_filter(self, config_file):
        return getattr(Image, config_file.compression_filter.upper())

    def get_fit_method(self, img, config_file):
        resize_fit = config_file.resize_fit
        return getattr(img, resize_fit)

    def resize_image(
        self, config_file, override, img, fit_method, compression_filter, height=None, width=None
    ):
        if config_file.resize_type == C.RESIZE_TYPE_PERCENTAGE and not override:
            resize_percentage = config_file.resize_percentage
            wsize = int(float(img.size[0]) * float(resize_percentage / 100))
            hsize = int(float(img.size[1]) * float(resize_percentage / 100))
            return fit_method((wsize, hsize), compression_filter)
        if height and width == 0:
            hpercent = height / float(img.size[1])
            wsize = int(float(img.size[0]) * float(hpercent))
            return fit_method((wsize, height), compression_filter)
        if width and height == 0:
            wpercent = width / float(img.size[0])
            hsize = int(float(img.size[1]) * float(wpercent))
            return fit_method((width, hsize), compression_filter)
        return fit_method((width, height), compression_filter)

    def get_convert_type(self, config_file, img):
        # Any extra options
        if not config_file.convert_type == C.CONVERT_TYPE_DEFAULT:
            return config_file.convert_type
        return img.format

    def get_prefix(self, config_file):
        prefix = config_file.rename_prefix
        if prefix:
            return prefix + "_"
        return ""

    def get_suffix(self, config_file):
        suffix = config_file.rename_suffix
        if suffix:
            return "_" + suffix
        return ""

    def fix_orientation(self, config_file, img):
        if config_file.fix_orientation:
            if "exif" in img.info:
                exif = img.info["exif"]
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == "Orientation":
                        break
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
                return img, exif
        return img, None

    def save_image(
        self, img, action_obj, compression_obj, prefix, suffix, filetype, image_quality, exif=None
    ):
        filename = get_filename(compression_obj.initial_file.file.name)
        file_path = (
            f"{action_obj}/{compression_obj.id}/compressed_files/"
            f"{prefix}{filename}{suffix}.{filetype}"
        )
        if filetype == CONVERT_TYPE_JPEG:
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, img)
            img = bg
        os.makedirs(f"{action_obj}/{compression_obj.id}/compressed_files/")
        if exif:
            img.save(
                file_path,
                str(filetype),
                optimize=True,
                quality=image_quality,
                exif=exif,
            )
        else:
            img.save(
                file_path,
                str(filetype),
                optimize=True,
                quality=image_quality,
            )
        logger.info(
            f"Image saved to {file_path} with filetype {filetype} and quality"
            f" {image_quality} and exif {exif}"
        )
        return img, file_path

    def full_optimized_web_package(
        self,
        images_zip,
        filename,
        device_type,
        action_obj,
        compression_obj,
        img,
        fit_method,
        compression_filter,
        prefix,
        suffix,
        filetype,
        image_quality,
    ):
        if not device_type == C.DEVICE_TYPE_DESKTOP:
            images_zip.extend(
                _device_package(
                    filename,
                    1920,
                    C.DEVICE_TYPE_DESKTOP,
                    action_obj,
                    compression_obj,
                    img,
                    fit_method,
                    compression_filter,
                    prefix,
                    suffix,
                    filetype,
                    image_quality,
                )
            )
        if not device_type == C.DEVICE_TYPE_TABLET:
            images_zip.extend(
                _device_package(
                    filename,
                    650,
                    C.DEVICE_TYPE_TABLET,
                    action_obj,
                    compression_obj,
                    img,
                    fit_method,
                    compression_filter,
                    prefix,
                    suffix,
                    filetype,
                    image_quality,
                )
            )
        if not device_type == C.DEVICE_TYPE_MOBILE:
            images_zip.extend(
                _device_package(
                    filename,
                    345,
                    C.DEVICE_TYPE_MOBILE,
                    action_obj,
                    compression_obj,
                    img,
                    fit_method,
                    compression_filter,
                    prefix,
                    suffix,
                    filetype,
                    image_quality,
                )
            )
        return images_zip

    def zip_package(self, filename, images_zip, prefix, suffix):
        if len(images_zip):
            zip_path = f"{prefix}optimized_package_{filename}{suffix}.zip"
            zip_file = ZipFile(zip_path, "w")
            for image in images_zip:
                zip_file.write(image)
                logger.info(f"Image {image} added to zip file {zip_path}")
            zip_file.close()
        return zip_path


def _device_package(
    filename,
    width,
    device_type,
    action_obj,
    compression_obj,
    img,
    fit_method,
    compression_filter,
    prefix,
    suffix,
    filetype,
    image_quality,
):
    images_zip = []
    wpercent = width / float(img.size[0])
    hsize = int(float(img.size[1]) * float(wpercent))
    img = fit_method((width, hsize), compression_filter)

    path = (
        f"{action_obj}/{compression_obj.id}/compressed_files/{prefix}"
        f"{filename}{suffix}_{device_type}.{str(filetype)}"
    )
    if filetype == CONVERT_TYPE_JPEG:
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, img)
        img = bg
    img.save(
        path,
        str(filetype),
        optimize=True,
        quality=int(image_quality),
    )
    logger.info(f"Image saved to {path} with filetype {filetype} and quality {image_quality}")
    images_zip.append(path)
    logger.info(f"Image {path} added to zip file {path}")
    return images_zip
