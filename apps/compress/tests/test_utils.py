from graphene_django.utils.testing import GraphQLTestCase

from ..utils import get_filename


class CompressUtilsTestCase(GraphQLTestCase):
    def test_get_filename(self):
        file_path = "C:/Users/username/Downloads/file.txt"
        self.assertEqual(get_filename(file_path), "file")
