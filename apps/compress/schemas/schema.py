import graphene

from apps.action.models import Action
from apps.action.schemas.schema import ActionType

from ..tasks import compress_action


class CompressAction(graphene.Mutation):
    verification_message = graphene.String()
    action = graphene.Field(ActionType)

    def mutate(self, info, **kwargs):
        request = info.context
        action_obj = Action.objects.new_or_get(request)
        if not action_obj.compressions.exists():
            verification_message = "You don't have any files to compress."
            return CompressAction(action=action_obj, verification_message=verification_message)
        # Loop through initial files and filter on status
        compress_action.delay(action_obj.id)
        verification_message = "We are compressing files"
        return CompressAction(action=action_obj, verification_message=verification_message)


class Mutation(graphene.ObjectType):
    compress_action = CompressAction.Field()
