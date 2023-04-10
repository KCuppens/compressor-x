import factory

from apps.initial_files.models import InitialFile


class InitialFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InitialFile

    file = "test_file.png"
