import os

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from apps.base.channels import CompressProgressConsumer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "compressorx.settings.production")
django_asgi_app = get_asgi_application()

websocket_urlpatterns = [
    path("progress/<str:action_id>/", CompressProgressConsumer.as_asgi()),
]
application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
