import logging

import graphene
from graphene_django import DjangoObjectType

from ..models import ConfigFile


logger = logging.getLogger(__name__)


class ConfigFileType(DjangoObjectType):
    class Meta:
        model = ConfigFile
        fields = "__all__"


class UpdateConfigFile(graphene.Mutation):
    config_file = graphene.Field(ConfigFileType)
    verification_message = graphene.String()

    class Arguments:
        id = graphene.String(required=True)
        custom = graphene.Boolean(required=True)
        lossless = graphene.Boolean(required=True)
        lossy = graphene.Boolean(required=True)
        resize_type = graphene.String()
        resize_percentage = graphene.Decimal()
        resize_width = graphene.Int()
        resize_height = graphene.Int()
        resize_fit = graphene.String()
        rename_prefix = graphene.String()
        rename_suffix = graphene.String()
        keep_exif = graphene.Boolean()
        fix_orientation = graphene.Boolean()
        image_quality = graphene.Decimal()
        compression_filter = graphene.String()
        keep_size = graphene.Boolean()
        device_type = graphene.String()
        maximum_file_size = graphene.Int()
        convert_type = graphene.String()
        full_optimized_web_package = graphene.Boolean()

    def mutate(self, info, **kwargs):
        id = kwargs.get("id")
        config_file = ConfigFile.objects.filter(id=id).update(**kwargs)
        verification_message = "Your config file has been updated."
        return UpdateConfigFile(config_file=config_file, verification_message=verification_message)


class Mutation(graphene.ObjectType):
    update_config_file = UpdateConfigFile.Field()
