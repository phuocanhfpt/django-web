from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class ChatConfig(models.Model):
    is_enabled = models.BooleanField(default=True, verbose_name="Bật chat")
    auto_reply_enabled = models.BooleanField(default=False, verbose_name="Bật trả lời tự động")
    auto_reply_message = models.TextField(blank=True, default="", verbose_name="Nội dung trả lời tự động")
    auto_reply_delay = models.PositiveIntegerField(default=30, verbose_name="Thời gian chờ trả lời tự động (giây)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cấu hình chat"
        verbose_name_plural = "Cấu hình chat"

    def __str__(self):
        return "Cấu hình chat"

    @classmethod
    def get_config(cls):
        config, created = cls.objects.get_or_create(pk=1)
        return config

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"Chat với {self.user.username}"
        return f"Chat với {self.guest_name or 'Khách'}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=100)
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"
