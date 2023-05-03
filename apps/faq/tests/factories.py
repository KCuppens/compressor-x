"""Factories for the FAQ app."""
import factory.fuzzy

from ..models import Question, Topic


class TopicFactory(factory.django.DjangoModelFactory):
    """Topic factory."""

    class Meta:
        """Meta class for TopicFactory."""

        model = Topic

    name = factory.fuzzy.FuzzyText(length=12)
    slug = factory.fuzzy.FuzzyText(length=12)
    description = factory.fuzzy.FuzzyText(length=36)
    image = factory.django.ImageField(color="blue")


class QuestionFactory(factory.django.DjangoModelFactory):
    """Question factory."""

    class Meta:
        """Meta class for QuestionFactory."""

        model = Question

    question = factory.fuzzy.FuzzyText(length=12)
    answer = factory.fuzzy.FuzzyText(length=12)
    topic = factory.SubFactory(TopicFactory)
