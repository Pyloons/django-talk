from django.contrib import admin
from .django_talk.models import ChatRoom


class ChatRoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(ChatRoom, ChatRoomAdmin)
