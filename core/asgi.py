import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter 
from room.routing import websocket_urlpatterns

from channels.middleware import BaseMiddleware
import logging

logger = logging.getLogger(__name__)

class DebugMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        logger.debug(f"Received scope: {scope}")
        return await super().__call__(scope, receive, send)
application =ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
app =application