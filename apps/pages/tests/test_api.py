"""Faq API tests."""
from django.contrib.contenttypes.models import ContentType

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase

from apps.locales.tests.factories import LocaleFactory
from apps.pages.models import Page, PageText
from apps.translations.models import Translation
from apps.users.tests.factories import UserFactory


class PageTestCase(JSONWebTokenTestCase):
    """Page API tests."""

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_page(self):
        """Create topic factory."""
        page = Page.objects.create(key_name="test", title="test", content="test")
        Translation.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_id=page.id,
            language="nl",
            field="title",
            text="title",
        )
        return page

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_page_text(self):
        """Create question factory."""
        page_text = PageText.objects.create(key_name="test", text="test")
        Translation.objects.create(
            content_type=ContentType.objects.get_for_model(PageText),
            object_id=page_text.id,
            language="nl",
            field="text",
            text="text",
        )
        return page_text

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_user(self):
        """Create user factory."""
        return UserFactory(is_staff=True)

    def setUp(self):
        """Set up test case."""
        LocaleFactory(is_default=True, code="en")
        LocaleFactory(code="nl")
        self.page = self.create_page()
        self.page_text = self.create_page_text()
        self.user = self.create_user()
        self.client.authenticate(self.user)

    def test_get_page_by_key_name(self):
        """Test get page by key name."""
        query = """
            query getPageByKeyName($keyName: String!, $lng: String){
                getPageByKeyName(keyName: $keyName, lng: $lng){
                    id
                }
            }
            """
        variables = {"keyName": "test"}
        response = self.client.execute(query, variables)
        self.assertEqual(response.data["getPageByKeyName"]["id"], str(self.page.id))

    def test_get_page_text_by_key_name(self):
        """Test get page text by key name."""
        query = """
            query getPageTextByKeyName($keyName: String!, $lng: String){
                getPageTextByKeyName(keyName: $keyName, lng: $lng){
                    text
                }
            }
            """
        variables = {"keyName": "test"}
        response = self.client.execute(query, variables)
        self.assertEqual(response.data["getPageTextByKeyName"]["text"], str(self.page_text.text))

    def test_get_page_by_key_name_locale(self):
        """Test get page by key name."""
        query = """
            query getPageByKeyName($keyName: String!, $lng: String){
                getPageByKeyName(keyName: $keyName, lng: $lng){
                    title
                }
            }
            """
        variables = {"keyName": "test", "lng": "nl"}
        response = self.client.execute(query, variables)
        self.assertEqual(response.data["getPageByKeyName"]["title"], "title")

    def test_get_page_text_by_key_name_locale(self):
        """Test get page text by key name."""
        query = """
            query getPageTextByKeyName($keyName: String!, $lng: String){
                getPageTextByKeyName(keyName: $keyName, lng: $lng){
                    text
                }
            }
            """
        variables = {"keyName": "test", "lng": "nl"}
        response = self.client.execute(query, variables)
        self.assertEqual(response.data["getPageTextByKeyName"]["text"], "text")
