import factory

from ..models import Compression


class CompressionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Compression
