"""Cookie schema."""
import logging

import graphene
from graphene_django import DjangoObjectType

from apps.base.constants import STATE_PUBLISHED
from apps.base.utils import models_to_dict

from ..models import AdBlock, Cookie


logger = logging.getLogger(__name__)


class CookieType(DjangoObjectType):
    """Cookie type."""

    class Meta:
        """Meta class for CookieType."""

        model = Cookie
        fields = "__all__"


class AdBlockType(DjangoObjectType):
    """AdBlock type."""

    class Meta:
        """Meta class for AdBlockType."""

        model = AdBlock
        fields = "__all__"


class Query(graphene.ObjectType):
    """Query class for cookie schema."""

    get_cookie = graphene.Field(CookieType, lng=graphene.String())
    get_adblock = graphene.Field(AdBlockType, lng=graphene.String())

    def resolve_get_cookie(self, info, lng: str = None):
        cookie = Cookie.objects.filter(state=STATE_PUBLISHED)
        logger.info(f"Get cookie: {models_to_dict(cookie)}")
        if lng:
            cookie = cookie.translate(lng)
            logger.info(f"Get translated cookie: {models_to_dict(cookie)}")
        return cookie.first()

    def resolve_get_adblock(self, info, lng: str = None):
        adblock = AdBlock.objects.filter(state=STATE_PUBLISHED)
        logger.info(f"Get adblock: {models_to_dict(adblock)}")
        if lng:
            adblock = adblock.translate(lng)
            logger.info(f"Get translated adblock: {models_to_dict(adblock)}")
        return adblock.first()
