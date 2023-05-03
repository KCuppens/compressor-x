"""Cookie schema."""
import logging

import graphene
from graphene_django import DjangoObjectType

from apps.base.constants import STATE_PUBLISHED
from apps.base.utils import models_to_dict

from ..models import Cookie


logger = logging.getLogger(__name__)


class CookieType(DjangoObjectType):
    """Cookie type."""

    class Meta:
        """Meta class for CookieType."""

        model = Cookie
        fields = "__all__"


class Query(graphene.ObjectType):
    """Query class for cookie schema."""

    get_cookie = graphene.Field(CookieType, lng=graphene.String())

    def resolve_get_cookie(self, info, lng: str = None):
        cookie = Cookie.objects.filter(state=STATE_PUBLISHED)
        logger.info(f"Get cookie: {models_to_dict(cookie)}")
        if lng:
            cookie = cookie.translate(lng)
            logger.info(f"Get translated cookie: {models_to_dict(cookie)}")
        return cookie.first()
