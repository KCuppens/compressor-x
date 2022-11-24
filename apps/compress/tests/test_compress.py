import os

import apps.data.constants as C
from apps.initial_file.models import InitialFile
from graphene_django.utils.testing import GraphQLTestCase

from apps.action.models import Action
from apps.compress.services.CompressEngine import CompressEngine


class CompressFileTestCase(GraphQLTestCase):
    def test_compress_file_action(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_custom_keep_size(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.keep_size = True
        action_obj.config_file.save(update_fields=["custom", "keep_size"])
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_custom_desktop_size(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.save(update_fields=["custom", "device_type", "resize_type"])
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_custom_tablet_size(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_TABLET
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.save(update_fields=["custom", "device_type", "resize_type"])
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_custom_mobile_size(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_MOBILE
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.save(update_fields=["custom", "device_type", "resize_type"])
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_custom_size(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_MOBILE
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.resize_width = 1920
        action_obj.config_file.resize_height = 1920
        action_obj.config_file.save(
            update_fields=[
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_resize_fit(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_MOBILE
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.resize_width = 1920
        action_obj.config_file.resize_height = 1920
        action_obj.config_file.resize_fit = C.FIT_TYPE_SCALE
        action_obj.config_file.save(
            update_fields=[
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
                "resize_fit",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_resize_type_nearest(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.compression_filter = C.FILTER_TYPE_NEAREST
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
                "resize_fit",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_resize_type_box(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.compression_filter = C.FILTER_TYPE_BOX
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
                "resize_fit",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_resize_type_bilinear(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.compression_filter = C.FILTER_TYPE_BILINEAR
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
                "resize_fit",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_resize_type_bicubic(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.compression_filter = C.FILTER_TYPE_BICUBIC
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
                "resize_fit",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_resize_type_lanczos(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.compression_filter = C.FILTER_TYPE_LANCZOS
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
                "resize_fit",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_resize_type_hamming(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.compression_filter = C.FILTER_TYPE_HAMMING
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "resize_width",
                "resize_height",
                "resize_fit",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_convert_type_webp(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.convert_type = C.CONVERT_TYPE_WEBP
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "convert_type",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_convert_type_png(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.convert_type = C.CONVERT_TYPE_PNG
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "convert_type",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_convert_type_jpg(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.convert_type = C.CONVERT_TYPE_JPEG
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "convert_type",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_rename_prefix(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.rename_prefix = "test"
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "convert_type",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_rename_suffix(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.rename_suffix = "test"
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "convert_type",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_keep_exif(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.keep_exif = True
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "keep_exif",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_no_exif(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.keep_exif = False
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "keep_exif",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."

    def test_compress_full_optimized_web_package(self):
        # Setup action and initial files
        action_obj = Action.objects.new()
        action_obj.config_file.custom = True
        action_obj.config_file.device_type = C.DEVICE_TYPE_DESKTOP
        action_obj.config_file.resize_type = C.RESIZE_TYPE_PIXELS
        action_obj.config_file.full_optimized_web_package = True
        action_obj.config_file.save(
            update_fields=[
                "compression_filter",
                "custom",
                "device_type",
                "resize_type",
                "full_optimized_web_package",
            ]
        )
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="jpg")
        action_obj.initial_files.add(initial_file)
        # Compress png file
        response = CompressEngine.compress(action_obj)
        assert response == "Succesfully converted all initial files."
