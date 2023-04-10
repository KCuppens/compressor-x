from django.test import TestCase

from ..models import Config
from .factories import ConfigFactory


class ConfigManagerTestCase(TestCase):
    def setUp(self):
        self.config = ConfigFactory()

    def test_get_config(self):
        self.assertEqual(
            self.config.value,
            Config.objects.get_config(self.config.key_name),
        )
