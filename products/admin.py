from django.contrib import admin
from .models import Category, Product, Brand, HeroSlide, Contact, FAQ, Promotion, UserProfile, ProductComment, Feature

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'status', 'show_on_home', 'created', 'updated']
    list_filter = ['status', 'show_on_home', 'created', 'updated']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'brand', 'price', 'sale_price', 
                   'has_wifi', 'has_night_vision', 'is_waterproof', 'featured', 
                   'status', 'created', 'updated']
    list_filter = ['status', 'featured', 'category', 'brand', 'has_wifi', 
                  'has_night_vision', 'is_waterproof', 'created', 'updated']
    list_editable = ['price', 'sale_price', 'featured', 'status']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['features']

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['title', 'description']
    list_editable = ['order', 'status']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'status']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'type', 'discount', 'start_date', 'end_date', 'status']
    list_filter = ['type', 'status', 'start_date', 'end_date']
    search_fields = ['name', 'code', 'description']
    list_editable = ['status']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone', 'is_email_verified']
    list_filter = ['is_email_verified']
    search_fields = ['user__username', 'full_name', 'phone']

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'content', 'created', 'approved', 'is_admin_reply', 'parent']
    list_filter = ['approved', 'is_admin_reply', 'created']
    search_fields = ['content', 'user__username', 'product__name']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Duyệt các bình luận đã chọn"

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'description']
    search_fields = ['name', 'description', 'icon']
