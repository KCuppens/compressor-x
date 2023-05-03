"""Faq schema module."""
import logging

import graphene
from graphene_django import DjangoObjectType

from apps.base.utils import models_to_dict

from ..models import Page, PageElement, PageText


logger = logging.getLogger(__name__)


class PageType(DjangoObjectType):
    """Page type."""

    class Meta:
        """Meta class for PageType."""

        model = Page
        fields = "__all__"

    def resolve_image(self, info):
        """Get image url."""
        return self.image.url or ""


class PageElementType(DjangoObjectType):
    """PageElement type."""

    class Meta:
        """Meta class for PageElementType."""

        model = PageElement
        fields = "__all__"

    def resolve_image(self, info):
        """Get image url."""
        return self.image.url or ""


class PageTextType(DjangoObjectType):
    """PageText type."""

    class Meta:
        """Meta class for PageTextType."""

        model = PageText
        fields = "__all__"

    def resolve_image(self, info):
        """Get image url."""
        return self.image.url or ""


class Query(graphene.ObjectType):
    """Query class for Page schema."""

    get_page_by_key_name = graphene.Field(
        PageType, key_name=graphene.String(), lng=graphene.String()
    )
    get_page_text_by_key_name = graphene.Field(
        PageTextType,
        key_name=graphene.String(),
        lng=graphene.String(),
    )

    def resolve_get_page_by_key_name(self, info, key_name, lng: str = None):
        """Get Page."""
        pages = Page.objects.filter(key_name=key_name)
        if lng:
            pages = pages.translate(lng)
            logger.info(f"Get page by key_name: {models_to_dict(pages)}")
        return pages.first()

    def resolve_get_page_text_by_key_name(self, info, key_name, lng: str = None):
        """Get PageText."""
        pages = PageText.objects.filter(key_name=key_name)
        if lng:
            pages = pages.translate(lng)
            logger.info(f"Get page text by key_name: {models_to_dict(pages)}")
        return pages.first()
