import factory.fuzzy

from ..models import Locale


class LocaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Locale

    code = factory.fuzzy.FuzzyChoice(["en", "nl", "fr"])
    name = factory.fuzzy.FuzzyChoice(["English", "Nederlands", "Frans"])
    is_active = True
