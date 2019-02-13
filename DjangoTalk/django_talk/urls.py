from .views import ChatView as chv
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<room_name>[^/]+)/$', chv.as_view(), name='chat-room'),
]
