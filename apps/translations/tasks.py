"""Create multiple tasks files for avoiding circular dependency import."""
import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

# Celery once makes sure a certain task only ran once at the same time,
# the lock will go away after successfull task
from celery_once import QueueOnce

from apps.locales.models import Locale
from compressorx.celery import app

from .deepl import Deepl
from .models import Translation


logger = logging.getLogger(__name__)


@app.task(
    base=QueueOnce,
    once={"graceful": True},
    name="translate_object",
    acks_late=True,
    autoretry_for=(Exception,),
    retry_backoff=3,
    retry_kwargs={"max_retries": 3},
    queue="default",
)
def translate_object(model, obj_id):
    """Translate translate fields of a model."""
    model = apps.get_model(model)
    obj = model.objects.get(id=obj_id)
    for field in model.get_translatable_fields():
        # Check if field is not empty
        value = field.value_from_object(obj)
        if value:
            # Loop through all languages except default
            for lang in Locale.objects.filter(is_active=True, is_default=False):
                # Check if translations exist
                translation = Translation.objects.filter(
                    content_type=ContentType.objects.get_for_model(model),
                    object_id=obj_id,
                    language=lang.code,
                    field=field.name,
                ).first()
                if not translation:
                    # If not exists create a translation based on deepl
                    Translation.objects.create(
                        content_type=ContentType.objects.get_for_model(model),
                        object_id=obj_id,
                        language=lang.code,
                        field=field.name,
                        text=Deepl().translate(value, lang.deepl_code),
                    )
