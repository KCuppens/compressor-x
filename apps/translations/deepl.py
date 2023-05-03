import logging

from django.conf import settings

import deepl


logger = logging.getLogger(__name__)


class Deepl:
    """Deepl translation service."""

    def __init__(self):
        """Initialize the Deepl service."""
        self.api_key = settings.DEEPL_API_KEY
        self.translator = deepl.Translator(self.api_key)
        self.default = "nl"

    def translate(self, text, target_lang):
        """Translate a text to a target language."""
        if self.translator:
            translation = self.translator.translate_text(
                text,
                target_lang=target_lang,
                source_lang=self.default,
                preserve_formatting=True,
            )
            logger.info(f"Translated {text} in {target_lang}: {translation}")
            return translation
        return None
