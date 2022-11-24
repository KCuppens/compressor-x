from django.db import transaction

from apps.action.models import Action
from apps.compress.services.CompressEngine import CompressEngine
from compressorx.celery import app


@transaction.atomic
@app.task(name="compress_action", queue="convert")
def compress_action(action_id):
    try:
        action_obj = Action.objects.filter(id=action_id).first()
        response = CompressEngine.compress(action_obj)
        return response
    except Exception as e:
        return f"There has been an error: {e}."
