import time

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.action.tests.factories import ActionFactory
from apps.base.storage_backends import MediaStorage
from apps.base.utils import CustomGraphQLTestCase
from apps.compression.tests.factories import CompressionFactory

from ..utils import get_initial_file_path, get_unique_file_name, uploading_initial_file


class InitialFileUtilsTestCase(CustomGraphQLTestCase):
    def test_get_unique_file_name(self):
        test_file = SimpleUploadedFile("assignment.jpg", b"content")
        file_name = get_unique_file_name(test_file)
        time.sleep(1)
        file_name_2 = get_unique_file_name(test_file)
        self.assertNotEqual(file_name, file_name_2)

    def test_get_initial_file_path(self):
        test_file = SimpleUploadedFile("assignment.jpg", b"content")
        action_obj = ActionFactory()
        compression_obj = CompressionFactory()
        filename = get_unique_file_name(test_file)
        path = get_initial_file_path(action_obj, compression_obj, filename)
        self.assertIn(f"{action_obj}/{compression_obj.id}/initial_files/", path)

    def test_uploading_initial_file(self):
        test_file = SimpleUploadedFile("assignment.jpg", b"content")
        action_obj = ActionFactory()
        initial_file = uploading_initial_file(test_file, action_obj)
        media_storage = MediaStorage()
        initial_file.refresh_from_db()
        path = str(initial_file.file)
        self.assertTrue(media_storage.exists(path))
        initial_file.file.delete()
        initial_file.delete()
        self.assertFalse(media_storage.exists(path))
