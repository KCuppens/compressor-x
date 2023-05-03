"""
Create multiple tasks files for avoiding circular dependency import
"""
import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

# Celery once makes sure a certain task only ran once at the same time,
# the lock will go away after successfull task
from celery_once import QueueOnce

from apps.translations.deepl import Deepl
from compressorx.celery import app


logger = logging.getLogger(__name__)


@app.task(
    base=QueueOnce,
    once={"graceful": True},
    name="translate_all_objects",
    acks_late=True,
    autoretry_for=(Exception,),
    retry_backoff=3,
    retry_kwargs={"max_retries": 3},
    queue="default",
)
def translate_all_objects(locale_id):
    """
    Translate translate fields of a model
    """
    from apps.translations.models import Translation

    from .models import Locale

    try:
        locale = Locale.objects.get(id=locale_id, is_default=False)
    except Locale.DoesNotExist:
        return
    models = [
        "blog.Blog",
        "pages.Page",
        "pages.PageElement",
        "pages.PageText",
        "cookies.Cookie",
        "faq.Topic",
        "faq.Question",
    ]
    for model in models:
        model: str = apps.get_model(model)
        objects = model.objects.all()
        for obj in objects:
            for field in model.get_translatable_fields():
                # Check if field is not empty
                value = field.value_from_object(obj)
                if value:
                    # Check if translations exist
                    translation = Translation.objects.filter(
                        content_type=ContentType.objects.get_for_model(model),
                        object_id=obj.id,
                        language=locale.code,
                        field=field.name,
                    ).first()
                    if not translation:
                        # If not exists create a translation based on deepl
                        Translation.objects.create(
                            content_type=ContentType.objects.get_for_model(model),
                            object_id=obj.id,
                            language=locale.code,
                            field=field.name,
                            text=Deepl().translate(value, locale.deepl_code),
                        )


@app.task(
    base=QueueOnce,
    once={"graceful": True},
    name="period_translate_all_objects",
    acks_late=True,
    autoretry_for=(Exception,),
    retry_backoff=3,
    retry_kwargs={"max_retries": 3},
    queue="default",
)
def period_translate_all_objects():
    """
    Translate translate fields of a model
    """
    from apps.translations.models import Translation

    from .models import Locale

    for locale in Locale.objects.filter(is_active=True, is_default=False):
        models = ["blog.Blog", "pages.Page", "services.Service", "text.Text", "products.Product"]
        for model in models:
            model = apps.get_model(model)
            objects = model.objects.all()
            for obj in objects:
                for field in model.get_translatable_fields():
                    # Check if field is not empty
                    value = field.value_from_object(obj)
                    if value:
                        # Check if translations exist
                        translation = Translation.objects.filter(
                            content_type=ContentType.objects.get_for_model(model),
                            object_id=obj.id,
                            language=locale.code,
                            field=field.name,
                        ).first()
                        if not translation:
                            # If not exists create a translation based on deepl
                            Translation.objects.create(
                                content_type=ContentType.objects.get_for_model(model),
                                object_id=obj.id,
                                language=locale.code,
                                field=field.name,
                                text=Deepl().translate(value, locale.deepl_code),
                            )
