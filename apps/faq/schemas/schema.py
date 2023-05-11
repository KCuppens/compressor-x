"""Faq schema module."""
import logging

import graphene
from graphene_django import DjangoObjectType

from apps.base.utils import models_to_dict

from ..models import Question, Topic


logger = logging.getLogger(__name__)


class QuestionType(DjangoObjectType):
    """Question type."""

    class Meta:
        """Meta class for QuestionType."""

        model = Question
        fields = "__all__"


class TopicType(DjangoObjectType):
    """Topic type."""

    questions = graphene.List(QuestionType)

    class Meta:
        """Meta class for TopicType."""

        model = Topic
        fields = "__all__"

    def resolve_image(self, info):
        """Get image url."""
        return self.image.url or ""

    def resolve_questions(self, info):
        """Get questions."""
        return self.questions.all().order_by("-position")


class Query(graphene.ObjectType):
    """Query class for faq schema."""

    get_topics = graphene.List(TopicType, lng=graphene.String())
    get_questions_by_topic = graphene.List(
        QuestionType, id=graphene.String(), lng=graphene.String()
    )
    get_questions = graphene.List(
        QuestionType,
        lng=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    def resolve_get_topics(self, info, lng: str = None):
        """Get topics."""
        topics = Topic.objects.all().order_by("-position")
        if lng:
            topics = topics.translate(lng)
            logger.info(f"Get translated topics: {models_to_dict(topics)}")
        return topics

    def resolve_get_questions(self, info, lng: str = None, limit=25, offset=0):
        """Get questions."""
        questions = Question.objects.all().order_by("-position")
        if lng:
            questions = questions.translate(lng)
            logger.info(f"Get translated questions: {models_to_dict(questions)}")
        return questions

    def resolve_get_questions_by_topic(
        self,
        info,
        id,
        lng: str = None,
    ):
        """Get questions by topic."""
        questions = Question.objects.filter(topic=id).order_by("-position")
        if lng:
            questions = questions.translate(lng)
            logger.info(f"Get translated questions: {models_to_dict(questions)}")
        return questions
