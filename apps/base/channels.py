from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class CompressProgressConsumer(AsyncWebsocketConsumer):
    """
    Websocket consumer for uploading files, compressing files
    """

    def celery_task_update(self, event):
        message = event["message"]
        self.send_json(message)

    def connect(self):
        super().connect()
        compress_id = self.scope.get("url_route").get("kwargs").get("compress_id")
        async_to_sync(self.channel_layer.group_add)(
            str("compress_" + str(compress_id)), self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        self.send(text_data="Hello world!")

    def disconnect(self, close_code):
        self.close()
