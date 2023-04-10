from itertools import chain

from django.utils.safestring import mark_safe

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from graphene_django.utils.testing import GraphQLTestCase

from .constants import ENVIRONMENT_COLORS
from .storage_backends import MediaStorage


def send_progress_websocket(action_obj, percentage, message, params={}):  # noqa: B006
    """
    Send a message to the websocket
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "compress_" + str(action_obj.id),
        {
            "compress_id": action_obj.id,
            "progress": percentage,
            "status": message,
            "params": params,
        },
    )


def get_environment_color(branch_name):
    if branch_name in ENVIRONMENT_COLORS:
        return ENVIRONMENT_COLORS[branch_name]
    return ENVIRONMENT_COLORS["other"]


def image_view(obj, height, width):
    if obj.image:
        return mark_safe(f'<img src="{obj.image.url}" width="{height}" height="{width}" />')
    return ""


def model_to_dict(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        if not getattr(f, "editable", False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


def models_to_dict(instances, fields=None, exclude=None):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    dict = {}
    for instance in instances:
        data = {}
        opts = instance._meta
        for f in chain(opts.concrete_fields, opts.private_fields):
            if not getattr(f, "editable", False):
                continue
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(instance)
        dict[instance.id] = data
    return data


class CustomGraphQLTestCase(GraphQLTestCase):
    """
    Overridden graphql URL, defaults to "/graphql".
    """

    GRAPHQL_URL = "/graphql/"


def upload_file_to_media(path, file):
    media_storage = MediaStorage()
    if not media_storage.exists(path):  # avoid overwriting existing file
        media_storage.save(path, file)
        return True
    return False
