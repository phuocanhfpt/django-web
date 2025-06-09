from django.contrib import admin
from .models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone', 'email', 'updated_at')
    search_fields = ('site_name', 'phone', 'email')
    readonly_fields = ('updated_at',)
