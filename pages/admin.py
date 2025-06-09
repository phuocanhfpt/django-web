from django.contrib import admin
from .models import SinglePage
from django.utils.text import slugify
from unidecode import unidecode

@admin.register(SinglePage)
class SinglePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('is_published',)
    readonly_fields = ('slug',)

    def save_model(self, request, obj, form, change):
        auto_slug = slugify(unidecode(obj.title))
        if not obj.slug or obj.slug == slugify(obj.title) or obj.slug == auto_slug:
            obj.slug = auto_slug
        super().save_model(request, obj, form, change)
