from datetime import datetime, timedelta

from app.celery import app

from apps.action.models import Action
import os
now = datetime.now()


# Delete action after 3 hours, run every 30 mins
@app.task(name="delete_expired_actions", queue="default")
def delete_expired_actions():
    actions = Action.objects.filter()
    count = 0
    for action in actions:
        if action.date_updated < (now - timedelta(hours=3)):
            try:
                # # Check if all initial files are deleted
                # if action.initial_files.exists():
                #     # Loop through initial files
                #     for file in action.initial_files.all():
                #         # Delete object
                #         file.delete()
                # # Check if all conversion files are deleted
                # if action.conversion_files.exists():
                #     # Loop through all conversion files
                #     for file in action.conversion_files.exists():
                #         # Delete object
                #         file.delete()
                # # Delete action object
                action.delete()
                count += 1
            except Exception:
                continue
    return f"There has been {count} actions deleted."
