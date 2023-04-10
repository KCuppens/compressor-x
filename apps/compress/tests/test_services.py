import os
from io import BytesIO

from django.core.files.storage import default_storage

from PIL import Image

import apps.config_file.constants as C
from apps.action.tests.factories import ActionFactory
from apps.base.utils import CustomGraphQLTestCase
from apps.compressed_file.utils import get_compressed_file_path
from apps.compression.models import Compression
from apps.config_file.constants import (
    DEVICE_TYPE_DESKTOP,
    IMAGE_QUALITY_LOSSLESS,
    IMAGE_QUALITY_LOSSY,
)
from apps.initial_files.tests.factories import InitialFileFactory

from ..services.AutoCompress import AutoCompress
from ..services.CustomCompress import CustomCompress, _device_package
from ..utils import get_filename


class AutoCompressTestCase(CustomGraphQLTestCase):
    def setUp(self):
        self.action = ActionFactory()
        self.config_file = self.action.config_file
        self.initial_file = InitialFileFactory()

    def test_image_quality_setting_lossless(self):
        self.assertEqual(AutoCompress().image_quality_setting(self.action), IMAGE_QUALITY_LOSSLESS)

    def test_image_quality_setting_lossy(self):
        self.config_file.lossy = True
        self.config_file.lossless = False
        self.config_file.save(update_fields=["lossy", "lossless"])

        self.assertEqual(AutoCompress().image_quality_setting(self.action), IMAGE_QUALITY_LOSSY)

    def test_image_quality_setting_custom(self):
        self.config_file.custom = True
        self.config_file.lossless = False
        self.config_file.image_quality = 99
        self.config_file.save(update_fields=["image_quality", "custom", "lossless"])
        self.assertEqual(AutoCompress().image_quality_setting(self.action), 99)

    def test_optimize_image(self):
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        image = AutoCompress().optimize_image(img, 99, self.initial_file)
        self.assertTrue(image)
        self.assertTrue(img.verify)
        os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))


class CustomCompressTestCase(CustomGraphQLTestCase):
    def setUp(self):
        self.action = ActionFactory()
        self.config_file = self.action.config_file
        self.initial_file = InitialFileFactory()

    def test_customize_size_custom(self):
        # Arrange
        self.config_file.resize_height = 100
        self.config_file.resize_width = 100
        self.config_file.save(update_fields=["resize_height", "resize_width"])
        # Act
        height, width, override = CustomCompress().customize_size(self.config_file)
        # Assert
        self.assertEqual(height, 100)
        self.assertEqual(width, 100)
        self.assertEqual(override, False)

    def test_customize_size_desktop(self):
        # Arrange
        self.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        self.config_file.save(update_fields=["device_type"])
        # Act
        height, width, override = CustomCompress().customize_size(self.config_file)
        # Assert
        self.assertEqual(height, 0)
        self.assertEqual(width, 1920)
        self.assertEqual(override, True)

    def test_customize_size_tablet(self):
        # Arrange
        self.config_file.device_type = C.DEVICE_TYPE_TABLET
        self.config_file.save(update_fields=["device_type"])
        # Act
        height, width, override = CustomCompress().customize_size(self.config_file)
        # Assert
        self.assertEqual(height, 0)
        self.assertEqual(width, 650)
        self.assertEqual(override, True)

    def test_customize_size_mobile(self):
        # Arrange
        self.config_file.device_type = C.DEVICE_TYPE_MOBILE
        self.config_file.save(update_fields=["device_type"])
        # Act
        height, width, override = CustomCompress().customize_size(self.config_file)
        # Assert
        self.assertEqual(height, 0)
        self.assertEqual(width, 345)
        self.assertEqual(override, True)

    def test_get_compression_filter(self):
        # Arrange
        # Act
        compression_filter = CustomCompress().get_compression_filter(self.config_file)
        # Assert
        self.assertTrue(compression_filter)

    def test_get_fit_method(self):
        # Arrange
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        # Act
        resize_fit = CustomCompress().get_fit_method(img, self.config_file)
        # Assert
        self.assertTrue(resize_fit)
        if os.path.exists("test_file.png"):
            os.remove("test_file.png")
        self.assertFalse(os.path.exists("test_file.png"))

    def test_resize_image_percentage(self):
        # Arrange
        self.config_file.resize_type = C.RESIZE_TYPE_PERCENTAGE
        self.config_file.resize_percentage = 50
        self.config_file.save(update_fields=["resize_type", "resize_percentage"])
        override = False
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        old_img = Image.open(BytesIO(file_content))
        fit_method = CustomCompress().get_fit_method(old_img, self.config_file)
        compression_filter = CustomCompress().get_compression_filter(self.config_file)
        # Act
        img = CustomCompress().resize_image(
            self.config_file, override, old_img, fit_method, compression_filter
        )
        # Assert
        self.assertEqual(int(old_img.size[0] / 2), int(img.size[0]))
        self.assertEqual(int(old_img.size[1] / 2), int(img.size[1]))
        if os.path.exists(get_compressed_file_path(self.initial_file)):
            os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))

    def test_resize_image_pixel(self):
        # Arrange
        self.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        self.config_file.save(update_fields=["resize_type"])
        override = True
        height = 500
        width = 500
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        old_img = Image.open(BytesIO(file_content))
        fit_method = CustomCompress().get_fit_method(old_img, self.config_file)
        compression_filter = CustomCompress().get_compression_filter(self.config_file)
        # Act
        img = CustomCompress().resize_image(
            self.config_file, override, old_img, fit_method, compression_filter, height, width
        )
        # Assert
        self.assertEqual(img.size[0], 500)
        self.assertEqual(img.size[1], 500)
        if os.path.exists(get_compressed_file_path(self.initial_file)):
            os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))

    def test_resize_image_pixel_auto_width(self):
        # Arrange
        self.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        self.config_file.save(update_fields=["resize_type"])
        override = True
        height = 500
        width = 0
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        old_img = Image.open(BytesIO(file_content))
        fit_method = CustomCompress().get_fit_method(old_img, self.config_file)
        compression_filter = CustomCompress().get_compression_filter(self.config_file)
        # Act
        img = CustomCompress().resize_image(
            self.config_file, override, old_img, fit_method, compression_filter, height, width
        )
        # Assert
        self.assertEqual(img.size[1], 500)
        self.assertNotEqual(img.size[0], 500)
        if os.path.exists(get_compressed_file_path(self.initial_file)):
            os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))

    def test_resize_image_pixel_auto_height(self):
        # Arrange
        self.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        self.config_file.save(update_fields=["resize_type"])
        override = True
        height = 0
        width = 500
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        old_img = Image.open(BytesIO(file_content))
        fit_method = CustomCompress().get_fit_method(old_img, self.config_file)
        compression_filter = CustomCompress().get_compression_filter(self.config_file)
        # Act
        img = CustomCompress().resize_image(
            self.config_file, override, old_img, fit_method, compression_filter, height, width
        )
        # Assert
        self.assertEqual(img.size[0], 500)
        self.assertNotEqual(img.size[1], 500)
        if os.path.exists(get_compressed_file_path(self.initial_file)):
            os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))

    def test_get_convert_type_jpeg(self):
        # Arrange
        self.config_file.convert_type = C.CONVERT_TYPE_JPEG
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        # Act
        file_type = CustomCompress().get_convert_type(self.config_file, img)
        # Assert
        self.assertEqual(file_type, "jpeg")
        if os.path.exists(get_compressed_file_path(self.initial_file)):
            os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))

    def test_get_convert_type_default(self):
        # Arrange
        self.config_file.convert_type = C.CONVERT_TYPE_DEFAULT
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        # Act
        file_type = CustomCompress().get_convert_type(self.config_file, img)
        # Assert
        self.assertEqual(file_type, img.format)
        if os.path.exists(get_compressed_file_path(self.initial_file)):
            os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))

    def test_get_prefix(self):
        # Arrange
        prefix_input = "test_prefix"
        self.config_file.rename_prefix = prefix_input
        self.config_file.save(update_fields=["rename_prefix"])
        # Act
        prefix = CustomCompress().get_prefix(self.config_file)
        # Assert
        self.assertEqual(prefix_input + "_", prefix)

    def test_get_suffix(self):
        # Arrange
        suffix_input = "test_suffix"
        self.config_file.rename_suffix = suffix_input
        self.config_file.save(update_fields=["rename_suffix"])
        # Act
        suffix = CustomCompress().get_suffix(self.config_file)
        # Assert
        self.assertEqual("_" + suffix_input, suffix)

    def test_fix_orientation(self):
        # Arrange
        self.config_file.fix_orientation = True
        self.config_file.save(update_fields=["fix_orientation"])
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        old_img = Image.open(BytesIO(file_content))
        # Act
        img, exif = CustomCompress().fix_orientation(self.config_file, old_img)
        # Assert
        self.assertTrue(old_img)
        if os.path.exists(get_compressed_file_path(self.initial_file)):
            os.remove(get_compressed_file_path(self.initial_file))
        self.assertFalse(os.path.exists(get_compressed_file_path(self.initial_file)))

    def test_save_image(self):
        # Arrange
        prefix = "test_prefix"
        suffix = "test_suffix"
        filetype = C.CONVERT_TYPE_JPEG
        image_quality = 80
        compression = Compression.objects.create(
            initial_file=self.initial_file,
        )
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        # Act
        img, file_path = CustomCompress().save_image(
            img, self.action, compression, prefix, suffix, filetype, image_quality
        )
        # Assert
        self.assertIn(prefix, file_path)
        self.assertIn(suffix, file_path)
        self.assertIn(filetype, file_path)
        filename = get_filename(compression.initial_file.file.name)
        if os.path.exists(
            f"{self.action.id}/{compression.id}/compressed_files/"
            f"{prefix}{filename}{suffix}.{filetype}"
        ):
            os.remove(
                f"{self.action.id}/{compression.id}/compressed_files/"
                f"{prefix}{filename}{suffix}.{filetype}"
            )
            os.removedirs(f"{self.action.id}/{compression.id}/compressed_files/")
        self.assertFalse(os.path.exists(f"{self.action.id}/{compression.id}/compressed_files/"))

    def test_full_optimized_web_package(self):
        prefix = "test_prefix"
        suffix = "test_suffix"
        filetype = C.CONVERT_TYPE_JPEG
        image_quality = 80
        compression = Compression.objects.create(
            initial_file=self.initial_file,
        )
        os.makedirs(f"{self.action.id}/{compression.id}/compressed_files/")
        filename = get_filename(compression.initial_file.file.name)
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        fit_method = CustomCompress().get_fit_method(img, self.config_file)
        compression_filter = CustomCompress().get_compression_filter(self.config_file)
        images_zip = CustomCompress().full_optimized_web_package(
            [],
            filename,
            None,
            self.action,
            compression,
            img,
            fit_method,
            compression_filter,
            prefix,
            suffix,
            filetype,
            image_quality,
        )
        self.assertEqual(len(images_zip), 3)
        for image in images_zip:
            self.assertTrue(os.path.exists(image))
            os.remove(image)
        os.removedirs(f"{self.action.id}/{compression.id}/compressed_files/")
        self.assertFalse(os.path.exists(f"{self.action.id}/{compression.id}/compressed_files/"))

    def test_zip_package(self):
        compression = Compression.objects.create(
            initial_file=self.initial_file,
        )
        filename = get_filename(compression.initial_file.file.name)
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        img.save(
            "test_file.png",
        )
        zip_path = CustomCompress().zip_package(filename, ["test_file.png"], "test_", "_test")
        self.assertTrue(os.path.exists(zip_path))
        self.assertEqual(zip_path.split(".")[-1], "zip")
        os.remove(zip_path)
        os.remove("test_file.png")
        self.assertFalse(os.path.exists(zip_path))
        self.assertFalse(os.path.exists("test_file.png"))

    def test__device_package(self):
        prefix = "test_prefix"
        suffix = "test_suffix"
        filetype = C.CONVERT_TYPE_JPEG
        image_quality = 80
        compression = Compression.objects.create(
            initial_file=self.initial_file,
        )
        os.makedirs(f"{self.action.id}/{compression.id}/compressed_files/")
        filename = get_filename(compression.initial_file.file.name)
        if not default_storage.exists(self.initial_file.file.name):
            AssertionError("File does not exist.")

        file_content = default_storage.open(self.initial_file.file.name).read()
        img = Image.open(BytesIO(file_content))
        fit_method = CustomCompress().get_fit_method(img, self.config_file)
        compression_filter = CustomCompress().get_compression_filter(self.config_file)
        images_zip = _device_package(
            filename,
            500,
            DEVICE_TYPE_DESKTOP,
            self.action,
            compression,
            img,
            fit_method,
            compression_filter,
            prefix,
            suffix,
            filetype,
            image_quality,
        )
        self.assertEqual(len(images_zip), 1)
        self.assertTrue(os.path.exists(images_zip[0]))
        os.remove(images_zip[0])
        os.removedirs(f"{self.action.id}/{compression.id}/compressed_files/")
        self.assertFalse(os.path.exists(f"{self.action.id}/{compression.id}/compressed_files/"))
        self.assertFalse(os.path.exists(images_zip[0]))
