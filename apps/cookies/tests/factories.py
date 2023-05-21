"""Factories for the cookies app."""
import factory.fuzzy

from ..models import AdBlock, Cookie


class CookieFactory(factory.django.DjangoModelFactory):
    """Cookie factory."""

    class Meta:
        """Meta class for CookieFactory."""

        model = Cookie

    title = factory.fuzzy.FuzzyText(length=12)
    message = factory.fuzzy.FuzzyText(length=48)
    essential_functional_cookies_description = factory.fuzzy.FuzzyText(length=48)
    analytical_cookies_description = factory.fuzzy.FuzzyText(length=48)
    external_content_cookies_description = factory.fuzzy.FuzzyText(length=48)


class AdBlockFactory(factory.django.DjangoModelFactory):
    """AdBlock factory."""

    class Meta:
        """Meta class for AdBlockFactory."""

        model = AdBlock

    title = factory.fuzzy.FuzzyText(length=12)
    message = factory.fuzzy.FuzzyText(length=48)
    button_text = factory.fuzzy.FuzzyText(length=12)
