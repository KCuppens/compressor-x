from unittest import mock

from django.contrib.contenttypes.models import ContentType

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase

from apps.base.constants import STATE_PUBLISHED
from apps.locales.tests.factories import LocaleFactory
from apps.translations.models import Translation
from apps.users.tests.factories import UserFactory

from ..models import Blog
from .factories import BlogFactory


class BlogTestCase(JSONWebTokenTestCase):
    """Blog API tests."""

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_blog(self):
        blog = BlogFactory(state=STATE_PUBLISHED)
        Translation.objects.create(
            content_type=ContentType.objects.get_for_model(Blog),
            object_id=blog.id,
            language="nl",
            field="name",
            text="name",
        )
        Translation.objects.create(
            content_type=ContentType.objects.get_for_model(Blog),
            object_id=blog.id,
            language="nl",
            field="slug",
            text="name",
        )
        return blog

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_user(self):
        """Create user factory."""
        return UserFactory(is_staff=True)

    @mock.patch("apps.locales.models.translate_all_objects.delay")
    def setUp(self, _):
        LocaleFactory(is_default=True, code="en")
        self.locale = LocaleFactory(is_active=True, code="nl")
        self.blog = self.create_blog()
        self.user = self.create_user()
        self.client.authenticate(self.user)

    def test_get_filter_blogs(self):
        """Test get filter blogs."""
        query = """
            query getFilterBlogs($name: String!) {
                getFilterBlogs(name: $name){
                    name,
                    id,
                    description,
                    keywords
                }
            }
            """
        variables = {"name": self.blog.name}
        response = self.client.execute(query, variables)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["getFilterBlogs"][0]["name"], self.blog.name)

    def test_get_filter_blogs_locale(self):
        query = """
            query getFilterBlogs($name: String!, $lng: String!) {
                getFilterBlogs(name: $name, lng: $lng){
                    name,
                    id,
                    description,
                    keywords,
                    image
                }
            }
            """
        variables = {"name": self.blog.name, "lng": self.locale.code}
        response = self.client.execute(query, variables)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["getFilterBlogs"][0]["name"], "name")

    def test_get_blog_detail(self):
        query = """
            query getBlogDetail($slug: String!) {
                getBlogDetail(slug: $slug){
                    name,
                    id,
                    description,
                    keywords,
                    image,
                }
            }
            """
        variables = {"slug": self.blog.slug}
        response = self.client.execute(query, variables)
        print(response)
        self.assertEqual(response.data["getBlogDetail"]["name"], self.blog.name)
        self.assertEqual(response.data["getBlogDetail"]["description"], self.blog.description)
        self.assertEqual(response.data["getBlogDetail"]["keywords"], self.blog.keywords)
        self.assertEqual(response.data["getBlogDetail"]["image"], self.blog.image.url)
        self.blog.image.delete()

    def test_get_blog_detail_locale(self):
        query = """
            query getBlogDetail($lng: String!, $slug: String!) {
                getBlogDetail(lng: $lng, slug: $slug){
                    name,
                    id,
                    description,
                    keywords
                }
            }
            """
        variables = {"lng": self.locale.code, "slug": "name"}
        response = self.client.execute(query, variables)
        self.assertEqual(response.data["getBlogDetail"]["name"], "name")
        self.assertEqual(response.data["getBlogDetail"]["description"], self.blog.description)
        self.assertEqual(response.data["getBlogDetail"]["keywords"], self.blog.keywords)
