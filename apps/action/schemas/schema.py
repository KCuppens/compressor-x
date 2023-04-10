import graphene
from graphene_django import DjangoObjectType

from ..models import Action


class ActionType(DjangoObjectType):
    class Meta:
        model = Action
        fields = "__all__"


class CreateOrGetAction(graphene.Mutation):
    action = graphene.Field(ActionType)
    verification_message = graphene.String()

    def mutate(self, info, **kwargs):
        request = info.context
        action_obj = Action.objects.new_or_get(request)
        verification_message = f"Successfully created action, {action_obj.id}"
        return CreateOrGetAction(action=action_obj, verification_message=verification_message)


class Mutation(graphene.ObjectType):
    create_or_get_action = CreateOrGetAction.Field()
