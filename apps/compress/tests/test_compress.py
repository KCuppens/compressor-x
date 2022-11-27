from apps.action.tests.factories import ActionFactory
from apps.base.storage_backends import MediaStorage
from apps.base.utils import CustomGraphQLTestCase
from apps.compress.services.CompressEngine import (
    CompressEngine,
    auto_compress,
    calculate_step_percentage,
    custom_compress,
)
from apps.compressed_file.models import CompressedFile
from apps.compression.models import Compression
from apps.initial_files.models import InitialFile


class CompressEngineTestCase(CustomGraphQLTestCase):
    def setUp(self):
        self.action = ActionFactory()
        self.config_file = self.action.config_file
        self.initial_file = InitialFile.objects.create(
            file="test_file.png",
        )
        self.compression = Compression.objects.create(
            initial_file=self.initial_file,
        )
        self.action.compressions.add(self.compression)
        self.media_storage = MediaStorage()

    def test_compress(self):
        self.assertEqual(
            CompressEngine().compress(self.action), "Succesfully completed the compression."
        )

    def test_check_supported_file_type(self):
        self.assertEqual(CompressEngine().check_supported_file_type(self.initial_file.file), True)

    def test_calculate_step_percentage(self):
        self.assertEqual(calculate_step_percentage(self.action.compressions.all()), 25)

    def test_auto_compress(self):
        compressed_file = auto_compress(self.action, self.compression, 0, 25)
        self.assertTrue(isinstance(compressed_file, CompressedFile))

    def test_custom_compress(self):
        compressed_file = custom_compress(self.action, self.compression, self.initial_file, 0, 25)
        self.assertTrue(isinstance(compressed_file, CompressedFile))
        compressed_file.file.delete()
