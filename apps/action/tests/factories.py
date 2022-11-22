import factory

from ..models import Action


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
