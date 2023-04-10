from django.core.files.uploadedfile import SimpleUploadedFile

from graphene_file_upload.django.testing import GraphQLFileUploadTestCase

from apps.action.models import Action
from apps.base.storage_backends import MediaStorage


class InitialFileTestCase(GraphQLFileUploadTestCase):
    def test_upload_file_to_initial_files(self):
        test_file = SimpleUploadedFile("assignment.jpg", b"content")
        response = self.file_query(
            """
            mutation uploadToInitialFiles($file: Upload!) {
                uploadToInitialFiles(file: $file) {
                    message,
                    action {
                        id
                    }
                }
            }
            """,
            op_name="uploadToInitialFiles",
            files={"file": test_file},
        )
        self.assertResponseNoErrors(response)
        self.assertTrue(response.json()["data"]["uploadToInitialFiles"]["action"]["id"])
        action_obj = Action.objects.get(
            id=response.json()["data"]["uploadToInitialFiles"]["action"]["id"]
        )
        compression_obj = action_obj.compressions.first()
        media_storage = MediaStorage()
        media_storage.delete(compression_obj.initial_file.file.name)
        self.assertFalse(media_storage.exists(compression_obj.initial_file.file.name))

    def test_upload_file_to_initial_files_unsupported(self):
        test_file = SimpleUploadedFile("assignment.txt", b"content")
        response = self.file_query(
            """
            mutation uploadToInitialFiles($file: Upload!) {
                uploadToInitialFiles(file: $file) {
                    message,
                    action {
                        id
                    }
                }
            }
            """,
            op_name="uploadToInitialFiles",
            files={"file": test_file},
        )
        assert (
            response.json()["data"]["uploadToInitialFiles"]["message"]
            == "We currently do not support this filetype. We will hurry!"
        )
