from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    objects = models.Manager()
    room_id = models.AutoField("房间号", primary_key=True)
    host = models.ForeignKey(User, verbose_name="频道主持人", default=None, related_name="be_hosts")
    channel_name = models.CharField("房间名", max_length=50)
    members = models.ManyToManyField(User, verbose_name="当前频道内成员", related_name="be_members", blank=True)
    black_list = models.ManyToManyField(User, verbose_name="黑名单", related_name="be_forbiden", blank=True)
    is_active = models.BooleanField("可用", default=True)

    def __str__(self):
        return self.channel_name
