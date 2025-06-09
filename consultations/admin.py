from django.contrib import admin
from .models import Consultation, Newsletter, FooterSettings, FooterMenuGroup, FooterMenu, Contact

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(FooterMenuGroup)
class FooterMenuGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'title')

@admin.register(FooterMenu)
class FooterMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'url', 'order', 'is_active', 'created_at')
    list_filter = ('group', 'is_active', 'created_at')
    search_fields = ('title', 'url')
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('group', 'order', 'title')

@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Thông tin công ty', {
            'fields': ('company_name', 'description', 'address')
        }),
        ('Thông tin liên hệ', {
            'fields': ('hotline', 'technical_support', 'business_phone', 'email', 'working_hours')
        }),
        ('Mạng xã hội', {
            'fields': ('facebook_url', 'youtube_url', 'instagram_url', 'tiktok_url', 'zalo_url')
        }),
        ('Bản quyền', {
            'fields': ('copyright_text',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # Chỉ cho phép tạo một bản ghi duy nhất
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
