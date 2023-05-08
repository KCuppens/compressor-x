from unittest import mock

from django.contrib.contenttypes.models import ContentType

import pytest

from apps.base.constants import STATE_PUBLISHED
from apps.base.utils import CustomGraphQLTestCase
from apps.locales.tests.factories import LocaleFactory
from apps.translations.models import Translation

from ..models import Cookie
from .factories import CookieFactory


class CookieTestcase(CustomGraphQLTestCase):
    """Cookie API tests."""

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_cookie(self):
        cookie = CookieFactory(state=STATE_PUBLISHED)
        Translation.objects.create(
            content_type=ContentType.objects.get_for_model(Cookie),
            object_id=cookie.id,
            language="nl",
            field="title",
            text="title",
        )
        return cookie

    @mock.patch("apps.locales.models.translate_all_objects.delay")
    def setUp(self, _):
        LocaleFactory(is_default=True, code="en")
        self.locale = LocaleFactory(is_active=True, code="nl")
        self.cookie = self.create_cookie()

    def test_get_cookie(self):
        """Test get cookie."""
        response = self.query(
            """
            query getCookie{
                getCookie{
                    title,
                    message,
                    essentialFunctionalCookiesDescription,
                    analyticalCookiesDescription,
                    externalContentCookiesDescription
                }
            }
            """
        )
        self.assertEqual(response.json()["data"]["getCookie"]["title"], self.cookie.title)
        self.assertEqual(response.json()["data"]["getCookie"]["message"], self.cookie.message)
        self.assertEqual(
            response.json()["data"]["getCookie"]["essentialFunctionalCookiesDescription"],
            self.cookie.essential_functional_cookies_description,
        )
        self.assertEqual(
            response.json()["data"]["getCookie"]["analyticalCookiesDescription"],
            self.cookie.analytical_cookies_description,
        )
        self.assertEqual(
            response.json()["data"]["getCookie"]["externalContentCookiesDescription"],
            self.cookie.external_content_cookies_description,
        )

    def test_get_cookie_locale(self):
        response = self.query(
            """
            query getCookie($lng: String!){
                getCookie(lng: $lng){
                    title,
                    message,
                    essentialFunctionalCookiesDescription,
                    analyticalCookiesDescription,
                    externalContentCookiesDescription
                }
            }
            """,
            variables={"lng": self.locale.code},
        )
        self.assertEqual(response.json()["data"]["getCookie"]["title"], "title")
        self.assertEqual(response.json()["data"]["getCookie"]["message"], self.cookie.message)
        self.assertEqual(
            response.json()["data"]["getCookie"]["essentialFunctionalCookiesDescription"],
            self.cookie.essential_functional_cookies_description,
        )
        self.assertEqual(
            response.json()["data"]["getCookie"]["analyticalCookiesDescription"],
            self.cookie.analytical_cookies_description,
        )
        self.assertEqual(
            response.json()["data"]["getCookie"]["externalContentCookiesDescription"],
            self.cookie.external_content_cookies_description,
        )

    def test_get_cookie_empty(self):
        """Test get cookie."""
        self.cookie.delete()
        response = self.query(
            """
            query getCookie{
                getCookie{
                    title,
                    message,
                    essentialFunctionalCookiesDescription,
                    analyticalCookiesDescription,
                    externalContentCookiesDescription
                }
            }
            """
        )
        self.assertEqual(response.json()["data"]["getCookie"], None)
