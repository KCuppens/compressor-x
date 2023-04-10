from datetime import datetime, timedelta

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from compressorx.celery import app

from .models import Action


now = datetime.now()


# Delete action after 6 hours, run every 30 mins
@app.task(name="delete_expired_actions", queue="default")
def delete_expired_actions():
    actions = Action.objects.filter()
    action_count = 0
    compression_count = 0
    for action in actions:
        if action.date_updated < (now - timedelta(hours=12)):
            for compression in action.compressions.all():
                # Check if all initial files are deleted
                if compression.initial_file:
                    # Delete object
                    compression.initial_file.file.delete()
                # Check if all conversion files are deleted
                if compression.compressed_file:
                    # Delete object
                    compression.compressed_file.file.delete()
                # Delete compression object
                compression.delete()
                compression_count += 1
            # Delete action object
            action.delete()
            action_count += 1
    return f"Deleted {action_count} actions and {compression_count} compressions"


schedule, _ = CrontabSchedule.objects.get_or_create(
    minute="30",
    hour="*",
    day_of_week="*",
    day_of_month="*",
    month_of_year="*",
)

PeriodicTask.objects.create(
    crontab=schedule,
    name="Delete expired actions",
    task="action.tasks.delete_expired_actions",
)
