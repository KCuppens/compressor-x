from apps.base.utils import CustomGraphQLTestCase


class ActionTestCase(CustomGraphQLTestCase):
    def test_create_or_get_action(self):
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
        print(response.json())
        assert response.json()["data"]["createOrGetAction"]["action"]["id"]

    def test_duplicate_create_or_get_action(self):
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
        print(response.json())
        assert response.json()["data"]["createOrGetAction"]["action"]["id"]
        id = response.json()["data"]["createOrGetAction"]["action"]["id"]
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
        print(response.json())
        assert response.json()["data"]["createOrGetAction"]["action"]["id"] == id
