from django.urls import path
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from users_chat.consumers import *
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^chat/(?P<otherId>[\d+]+)/$", ChatConsumer),
                ]
            )
        )
    )
})