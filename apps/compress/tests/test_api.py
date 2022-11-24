import os

from apps.initial_file.models import InitialFile
from graphene_django.utils.testing import GraphQLTestCase

from apps.action.models import Action


class CompressTestCase(GraphQLTestCase):
    def test_compress_action(self):
        response = self.query(
            """
            mutation createOrGetAction{
                createOrGetAction{
                    action {
                    id
                    }
                }
            }
            """,
        )
        id = response.json()["data"]["createOrGetAction"]["action"]["id"]
        assert id
        # Create initial files
        action_obj = Action.objects.filter(id=id).first()
        test_png = os.path.abspath("media/test_files/test_jpg.jpg")
        initial_file = InitialFile.objects.create(file=test_png, s3_url="test", mimetype="pdf")
        action_obj.initial_files.add(initial_file)
        response = self.query(
            """
            mutation compressAction{
                compressAction{
                    action {
                        id
                    },
                    verificationMessage
                }
            }
            """,
        )
        print(response.json())
        assert response.json()["data"]["compressAction"]["action"]["id"]
        assert (
            response.json()["data"]["compressAction"]["verificationMessage"]
            == "We are compressing files"
        )
