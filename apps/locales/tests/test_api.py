from graphql_jwt.testcases import JSONWebTokenTestCase

from .factories import LocaleFactory


class LocaleTestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.locale = LocaleFactory(is_default=True, code="en")

    def test_get_locales(self):
        query = """
            query getLocales{
                getLocales{
                    name,
                    code
                }
            }
            """
        response = self.client.execute(query)
        print(response)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["getLocales"][0]["name"], self.locale.name)
        self.assertEqual(response.data["getLocales"][0]["code"], self.locale.code)
