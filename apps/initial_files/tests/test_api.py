from django.core.files.uploadedfile import SimpleUploadedFile

from graphene_file_upload.django.testing import GraphQLFileUploadTestCase


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
        print(response.json())
        self.assertResponseNoErrors(response)
        self.assertTrue(response.json()["data"]["uploadToInitialFiles"]["action"]["id"])

    # def test_upload_file_to_initial_files_unsupported(self):
    #     test_file = SimpleUploadedFile("assignment.txt", b"content")
    #     response = self.file_query(
    #         """
    #         mutation uploadToInitialFiles($file: Upload!) {
    #             uploadToInitialFiles(file: $file) {
    #                 message,
    #                 action {
    #                     id
    #                 }
    #             }
    #         }
    #         """,
    #         op_name="uploadToInitialFiles",
    #         files={"file": test_file},
    #     )
    #     assert (
    #         response.json()["data"]["uploadToInitialFiles"]["message"]
    #         == "We currently do not support this filetype. We will hurry!"
    #     )
