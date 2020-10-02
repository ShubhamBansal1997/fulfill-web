# Third Party Stuff
import celery_progress.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            celery_progress.routing.websocket_urlpatterns
        )
    ),
})
