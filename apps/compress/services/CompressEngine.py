import os

from PIL import Image as PillImage

import apps.initial_files.constants as C
from apps.base.utils import send_progress_websocket
from apps.compress.services.AutoCompress import AutoCompress
from apps.compress.services.CustomCompress import CustomCompress
from apps.compress.utils import get_filename
from apps.compressed_file.models import CompressedFile
from apps.compressed_file.utils import get_compressed_file_path


class CompressEngine:
    def compress(self, action_obj):
        config_file = action_obj.config_file
        # Initial status in websocket
        send_progress_websocket(action_obj, 0, "Initializing compression")
        # Loop through compressions
        compressions = action_obj.compressions.all()
        step = calculate_step_percentage(compressions)
        count = 0
        for compression in compressions:
            init_file = compression.initial_file
            if config_file.custom:
                compression_file = custom_compress(action_obj, compression, init_file, count, step)
            else:
                compression_file = auto_compress(action_obj, compression, count, step)
            # File is compressed, update status to closed
            init_file.status = C.STATUS_CLOSED
            init_file.save(update_fields=["status"])
            # Mark compression file closed
            compression_file.status = C.STATUS_CLOSED
            compression_file.save(update_fields=["status"])
            # Websocket status to file completed
            send_progress_websocket(
                action_obj, count + step, "File compressed", {"file": init_file.id}
            ),
            count += step
        # Update status
        send_progress_websocket(action_obj, 100, "Compression completed.")
        return "Succesfully completed the compression."

    def check_supported_file_type(self, file):
        file_name = file.name.split("/")[-1]
        extension = file_name.split(".")[1]
        if extension in ["jpg", "jpeg", "png", "gif", "webp"]:
            return True
        return False


def calculate_step_percentage(compressions):
    return 100 / len(compressions) / 4


def auto_compress(action_obj, compression_obj, count, step):
    # Update status
    send_progress_websocket(
        action_obj,
        count + step,
        "Initializing.",
    )
    count += step
    init_file = compression_obj.initial_file
    img = PillImage.open(init_file.file)
    # Image quality setting
    image_quality = AutoCompress().image_quality_setting(action_obj)
    # Optimize image
    AutoCompress().optimize_image(img, image_quality, init_file)
    # Websocket status
    send_progress_websocket(
        action_obj,
        count + step,
        "Image optimized.",
    )
    # Create conversion file
    compression_file = CompressedFile.objects.create(
        file=get_compressed_file_path(init_file),
    )
    compression_obj.compressed_file = compression_file
    compression_obj.save(update_fields=["compressed_file"])
    # Update status
    send_progress_websocket(action_obj, count + step, "Compression file created.")
    count += step
    return compression_file


def custom_compress(action_obj, compression_obj, init_file, count, step):
    # Update status
    send_progress_websocket(
        action_obj,
        count + step,
        "Initializing.",
    )
    count += step
    img = PillImage.open(init_file.file)
    config_file = action_obj.config_file
    # Customize size
    height, width, override = CustomCompress().customize_size(config_file)
    # Setting variables

    resize_fit = CustomCompress().get_fit_method(img, config_file)
    compression_filter = CustomCompress().get_compression_filter(config_file)
    image_quality = config_file.image_quality
    convert_type = CustomCompress().get_convert_type(config_file, img)
    suffix = CustomCompress().get_suffix(config_file)
    prefix = CustomCompress().get_prefix(config_file)
    device_type = config_file.device_type
    # Resize image
    img = CustomCompress().resize_image(
        config_file, override, img, resize_fit, compression_filter, height, width
    )
    # Websocket status
    send_progress_websocket(
        action_obj,
        count + step,
        "Image optimized.",
    )
    if config_file.keep_exif and "exif" in img.info:
        img, exif = CustomCompress().fix_orientation(config_file, img)
        data = list(img.getdata())
        image = PillImage.new(img.mode, img.size)
        image.putdata(data)
        file, file_path = CustomCompress().save_image(
            image, action_obj, compression_obj, prefix, suffix, convert_type, image_quality, exif
        )
    else:
        file, file_path = CustomCompress().save_image(
            img, action_obj, compression_obj, prefix, suffix, convert_type, image_quality
        )
        print(file_path)

    if config_file.full_optimized_web_package:
        images_zip = [
            file,
        ]
        filename = get_filename(compression_obj.initial_file.file.name)
        images_zip = CustomCompress().full_optimized_web_package(
            images_zip,
            filename,
            device_type,
            action_obj,
            compression_obj,
            img,
            resize_fit,
            compression_filter,
            prefix,
            suffix,
            convert_type,
            image_quality,
            exif,
        )
        file_path = CustomCompress().zip_package(filename, images_zip, prefix, suffix, filename)

    # Websocket status
    send_progress_websocket(
        action_obj,
        count + step,
        "Image optimized.",
    )
    # Create conversion file
    compression_file = CompressedFile.objects.create(
        file=file_path,
    )
    os.remove(file_path)
    os.removedirs(f"{action_obj}/{compression_obj.id}/compressed_files/")
    compression_obj.compressed_file = compression_file
    compression_obj.save(update_fields=["compressed_file"])
    # Update status
    send_progress_websocket(action_obj, count + step, "Compression file created.")
    count += step
    return compression_file
