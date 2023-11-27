import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter 
from room.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

application =ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket":
    AllowedHostsOriginValidator( 
        AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ))
   
})
app =application