from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'email', 'phone', 'city', 'status', 'created']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['id', 'full_name', 'email', 'phone', 'address']
    inlines = [OrderItemInline]
    date_hierarchy = 'created'
