"""Faq API tests."""
import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase

from apps.locales.tests.factories import LocaleFactory
from apps.users.tests.factories import UserFactory

from .factories import QuestionFactory, TopicFactory


class FaqTestCase(JSONWebTokenTestCase):
    """Faq API tests."""

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_topic(self):
        """Create topic factory."""
        return TopicFactory()

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_question(self):
        """Create question factory."""
        return QuestionFactory(topic=self.topic)

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_user(self):
        """Create user factory."""
        return UserFactory(is_staff=True)

    def setUp(self):
        """Set up test case."""
        LocaleFactory(is_default=True, code="en")
        self.topic = self.create_topic()
        self.question = self.create_question()
        self.user = self.create_user()
        self.client.authenticate(self.user)

    def test_get_topics(self):
        """Test get topics."""
        query = """
            query getTopics{
                getTopics{
                    id,
                    image,
                    questions{
                        question,
                        answer
                    }
                }
            }
            """
        response = self.client.execute(query)
        self.assertEqual(response.data["getTopics"][0]["id"], str(self.topic.id))
        self.assertEqual(response.data["getTopics"][0]["image"], str(self.topic.image.url))
        self.topic.image.delete()

    def test_get_questions(self):
        """Test get questions."""
        query = """
            query getQuestions{
                getQuestions{
                    id
                }
            }
            """
        response = self.client.execute(query)
        self.assertEqual(response.data["getQuestions"][0]["id"], str(self.question.id))

    def test_get_questions_by_topic(self):
        """Test get questions by topic."""
        query = """
            query getQuestionsByTopic($id: String!){
                getQuestionsByTopic(id: $id){
                    id
                }
            }
            """
        variables = {"id": str(self.topic.id)}
        response = self.client.execute(query, variables)
        print(response)
        self.assertEqual(response.data["getQuestionsByTopic"][0]["id"], str(self.question.id))
