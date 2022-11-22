from apps.action.tests.factories import ActionFactory
from apps.base.utils import CustomGraphQLTestCase


class ActionModelsTestCase(CustomGraphQLTestCase):
    def test_new(self):
        action_obj = ActionFactory()
        assert action_obj.id
        # assert action_obj.config_file.id

    def test_action_str_id(self):
        action_obj = ActionFactory()
        assert action_obj.__str__() == str(action_obj.id)
