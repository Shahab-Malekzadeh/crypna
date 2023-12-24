"""
module docstring
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from .consumers import ChatConsumer

# It's much like a urls.py to route the user to the right url
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                    # url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),
                    # This should be match the url => 127.0.0.1:8000/index/
                    # Add all pages that you want to show the cryptocurrency prices
                    path("", ChatConsumer),
                    path("index/", ChatConsumer),
                    path("article/<slug:slug>/", ChatConsumer),
                    path("category/<slug:slug>/", ChatConsumer),
                    path("author/<slug:slug>/", ChatConsumer),
                    path("preview/<int:pk>/", ChatConsumer),
                ])
        ),
    ),
})
