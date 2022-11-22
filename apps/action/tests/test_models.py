from graphene_django.utils.testing import GraphQLTestCase

from apps.action.models import Action


class ActionModelsTestCase(GraphQLTestCase):
    def test_new(self):
        action_obj = Action.objects.new()
        assert action_obj.id
        assert action_obj.config_file.id

    def test_action_str_id(self):
        action_obj = Action.objects.new()
        assert action_obj.__str__() == str(action_obj.id)
