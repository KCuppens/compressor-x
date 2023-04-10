import factory

from apps.action.models import Action


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
