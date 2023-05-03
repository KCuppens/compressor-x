"""Blog schema module."""
import logging

from django.db.models import Q

import graphene
from graphene_django import DjangoObjectType

from apps.base.constants import STATE_PUBLISHED
from apps.base.utils import models_to_dict

from ..models import Blog


logger = logging.getLogger(__name__)


class BlogType(DjangoObjectType):
    """Blog type."""

    class Meta:
        """Meta class for BlogType."""

        model = Blog
        fields = "__all__"

    def resolve_image(self, info):
        """Return image url"""
        return self.image.url or ""


class Query(graphene.ObjectType):
    """Query class for blog schema."""

    get_filter_blogs = graphene.List(
        BlogType,
        name=graphene.String(),
        lng=graphene.String(),
        sort=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )
    get_blog_detail = graphene.Field(BlogType, slug=graphene.String(), lng=graphene.String())

    def resolve_get_blog_detail(self, info, slug, lng: str = None):
        blogs = Blog.objects.all()
        if lng:
            blogs = blogs.distinct().probe(lng)
        blogs = blogs.filter(slug=slug, state=STATE_PUBLISHED)
        logger.info(f"Get blog detail: {models_to_dict(blogs)}")
        if lng:
            logger.info(f"Get translated blog detail: {models_to_dict(blogs)}")
            return blogs.translate(lng).first()
        return blogs.first()

    def resolve_get_filter_blogs(
        self,
        info,
        name=None,
        lng: str = None,
        sort="date_desc",
        limit=25,
        offset=0,
    ):
        blogs = Blog.objects.filter(state=STATE_PUBLISHED)
        if name:
            blogs = blogs.filter(
                Q(name__contains=name)
                | Q(description__contains=name)
                | Q(slug__contains=name)
                | Q(keywords__contains=name)
            )
            logger.info(f"Get blogs by name: {models_to_dict(blogs)}")
        if lng:
            blogs = blogs.translate(lng)
            logger.info(f"Get translated blogs: {models_to_dict(blogs)}")
        return blogs[offset : offset + limit]  # noqa E203
