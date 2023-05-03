import logging

import graphene
from graphene_django import DjangoObjectType

from ..models import Locale


logger = logging.getLogger(__name__)


class LocaleType(DjangoObjectType):
    class Meta:
        model = Locale
        fields = "__all__"


class Query(graphene.ObjectType):
    get_locales = graphene.List(LocaleType)

    def resolve_get_locales(self, info):
        return Locale.objects.filter(is_active=True)
