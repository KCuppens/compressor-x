from django.db import models


class ActionManager(models.Manager):
    def new_or_get(self, request):
        if "action" in request.session:
            action_session = request.session["action"]
            action_obj = self.get(id=action_session)
        else:
            action_obj = self.create()
            request.session["action"] = str(action_obj.id)
        return action_obj
