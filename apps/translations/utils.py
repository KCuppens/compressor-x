"""This module contains the utilities for the Translations app."""

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query import prefetch_related_objects
from django.utils.functional import SimpleLazyObject

import apps.translations.models
from apps.base.utils import check_tables
from apps.locales.models import Locale


__docformat__ = "restructuredtext"


def _get_reverse_relation(model, relation):
    """Return the reverse of a model's relation."""
    parts = relation.split(LOOKUP_SEP)
    root = parts[0]
    branch = parts[1:]

    field = model._meta.get_field(root)
    reverse_relation = field.remote_field.name

    if branch:
        branch_model = field.related_model
        branch_relation = LOOKUP_SEP.join(branch)
        branch_reverse_relation = _get_reverse_relation(branch_model, branch_relation)
        return "{}__{}".format(
            branch_reverse_relation,
            reverse_relation,
        )
    else:
        return reverse_relation


def _get_dissected_lookup(model, lookup):
    """Return the dissected info of a lookup."""
    dissected = {
        "relation": [],
        "field": "",
        "supplement": "",
        "translatable": False,
    }

    def __get_dissected_field(root, model):
        """Return the dissected info of a field."""
        if root == "pk":
            return model._meta.pk
        else:
            return model._meta.get_field(root)

    def ___handle_field_model(field_model, root):
        """Handle field model and return dissected dict."""
        if field_model:
            dissected["relation"].append(root)
        else:
            dissected["field"] = root
            if (
                issubclass(model, apps.translations.models.Translatable)
                and root in model._get_translatable_fields_names()
            ):
                dissected["translatable"] = True

    def ___handle_nest(field_model, nest):
        """Handle nest and return dissected dict."""
        if field_model and nest:
            _fill_dissected(field_model, *nest)
        elif len(nest) == 1:
            dissected["supplement"] = nest[0]
        else:
            return None

    def _fill_dissected(model, *relation_parts):
        """Fill the dissected info of a lookup."""
        root = relation_parts[0]
        nest = relation_parts[1:]
        try:
            field = __get_dissected_field(root, model)
        except Exception as e:
            if not dissected["relation"] or nest or dissected["field"]:
                raise e
            dissected["supplement"] = root

        field_model = field.related_model
        ___handle_field_model(field_model, root)
        ___handle_nest(field_model, nest)

    parts = lookup.split(LOOKUP_SEP)

    _fill_dissected(model, *parts)

    return dissected


def _get_relations_hierarchy(*relations):
    """Return the relations hierarchy of some relations."""
    hierarchy = {}

    def _fill_hierarchy(hierarchy, *relation_parts):
        """Fill the relations hierarchy of some relations."""
        root = relation_parts[0]
        nest = relation_parts[1:]

        hierarchy.setdefault(
            root,
            {
                "included": False,
                "relations": {},
            },
        )

        if nest:
            _fill_hierarchy(hierarchy[root]["relations"], *nest)
        else:
            hierarchy[root]["included"] = True

    for relation in relations:
        parts = relation.split(LOOKUP_SEP)
        _fill_hierarchy(hierarchy, *parts)

    return hierarchy


def _get_entity_details(entity):
    """Return the iteration and type details of an entity."""
    error_message = SimpleLazyObject(
        lambda: "`{}` is neither {} nor {}.".format(
            entity,
            "a model instance",
            "an iterable of model instances",
        )
    )

    if isinstance(entity, models.Model):
        model = type(entity)
        iterable = False
    elif hasattr(entity, "__iter__"):
        if len(entity) > 0:
            if isinstance(entity[0], models.Model):
                model = type(entity[0])
            else:
                raise TypeError(error_message)
        else:
            model = None
        iterable = True
    else:
        raise TypeError(error_message)

    return (iterable, model)


def _get_purview(entity, hierarchy):
    """Return the purview of an entity and a relations hierarchy of it."""
    mapping = {}
    query = models.Q()

    def _fill_entity(entity, hierarchy, included=True):
        """Fill the purview of an entity and a relations hierarchy of it."""
        iterable, model = _get_entity_details(entity)
        if not model:
            return

        content_type_id = ContentType.objects.get_for_model(model).id
        instances = mapping.setdefault(content_type_id, {})

        if included and not issubclass(model, apps.translations.models.Translatable):
            raise TypeError("`{}` is not Translatable!".format(model))

        def ___fill_default_translatable_fields(obj):
            """Fill the default translatable fields of an object."""
            if not hasattr(obj, "_default_translatable_fields"):
                obj._default_translatable_fields = {
                    field: getattr(obj, field)
                    for field in type(obj)._get_translatable_fields_names()
                }
            return obj

        def __fill_query(obj):
            """Fill the query of an object."""
            if included:
                if not hasattr(obj, "_default_translatable_fields"):
                    obj._default_translatable_fields = {
                        field: getattr(obj, field)
                        for field in type(obj)._get_translatable_fields_names()
                    }
                object_id = obj.pk
                instances[object_id] = obj
                nonlocal query
                query |= models.Q(
                    content_type__id=content_type_id,
                    object_id=object_id,
                )

        def __handle_model_manager(relation, value):
            """Handle model manager and return the value."""
            if isinstance(value, models.Manager):
                if not (
                    hasattr(obj, "_prefetched_objects_cache")
                    and relation in obj._prefetched_objects_cache
                ):
                    prefetch_related_objects([obj], relation)
                return value.all()
            return value

        def _fill_obj(obj):
            __fill_query(obj)

            if hierarchy:
                for relation, detail in hierarchy.items():
                    value = getattr(obj, relation, None)
                    if value:
                        value = __handle_model_manager(relation, value)
                        _fill_entity(
                            entity=value,
                            hierarchy=detail["relations"],
                            included=detail["included"],
                        )

        if iterable:
            for obj in entity:
                _fill_obj(obj)
        else:
            _fill_obj(entity)

    _fill_entity(entity, hierarchy)

    return mapping, query


def _get_translations(query, lang):
    """Return the `Translation` queryset of a query in a language."""
    if query:
        queryset = (
            apps.translations.models.Translation.objects.filter(
                language=lang,
            )
            .filter(
                query,
            )
            .select_related("content_type")
        )

        return queryset
    else:
        return apps.translations.models.Translation.objects.none()


def validate_language(lng):
    """Validate a language code."""
    if lng and not check_if_language_exists(lng):
        return False
    return True


def check_if_language_exists(lng):
    """Check if a language code exists."""
    exists = False
    for lang in Locale.objects.filter(is_active=True):
        if lang.code == lng:
            exists = True
            break
    return exists


def get_languages():
    if not check_tables("locales_locale"):
        return (("en", "English"),)
    languages = []
    for lang in Locale.objects.filter(is_active=True):
        languages.append((lang.code, lang.name))
    return languages


def get_active_languages():
    if not check_tables("locales_locale"):
        return (("en", "English"),)
    languages = []
    for lang in Locale.objects.filter(is_active=True):
        languages.append(lang.code)
    return languages
