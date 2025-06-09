from django.contrib import admin
from .models import Conversation, Message, ChatConfig

@admin.register(ChatConfig)
class ChatConfigAdmin(admin.ModelAdmin):
    list_display = ('is_enabled', 'auto_reply_enabled', 'updated_at')
    list_editable = ('is_enabled', 'auto_reply_enabled')
    list_display_links = ('updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Cấu hình', {
            'fields': ('is_enabled', 'auto_reply_enabled', 'auto_reply_message', 'auto_reply_delay')
        }),
        ('Thông tin', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Chỉ cho phép tạo 1 bản ghi
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Không cho phép xóa
        return False

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'guest_name', 'created', 'last_active', 'is_closed')
    list_filter = ('is_closed', 'created', 'last_active')
    search_fields = ('user__username', 'guest_name')
    ordering = ('-last_active',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'is_admin', 'content', 'timestamp')
    list_filter = ('is_admin', 'timestamp')
    search_fields = ('sender', 'content', 'conversation__id')
