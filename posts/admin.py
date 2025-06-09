from django.contrib import admin
from .models import Post, PostCategory, Comment

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created']
    list_filter = ['category', 'status', 'created']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'content', 'created', 'approved', 'is_admin_reply', 'parent']
    list_filter = ['approved', 'is_admin_reply', 'created']
    search_fields = ['content', 'user__username', 'post__title']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Duyệt các bình luận đã chọn"
