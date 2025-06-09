from django.urls import path
from .views import chat_view, admin_conversation_list, admin_conversation_detail, get_or_create_conversation, send_message, get_messages, admin_unread_count, admin_latest_unread_conversation, admin_unread_list, customer_unread_count

app_name = 'chat'

urlpatterns = [
    path('<int:user_id>/', chat_view, name='chat_view'),
    path('admin/', admin_conversation_list, name='admin_conversation_list'),
    path('admin/<int:conversation_id>/', admin_conversation_detail, name='admin_conversation_detail'),
    path('get-or-create-conversation/', get_or_create_conversation, name='get_or_create_conversation'),
    path('api/send/', send_message, name='send_message'),
    path('api/messages/<int:conversation_id>/', get_messages, name='get_messages'),
    path('api/admin-unread/', admin_unread_count, name='admin_unread_count'),
    path('api/admin-latest-unread/', admin_latest_unread_conversation, name='admin_latest_unread_conversation'),
    path('api/admin-unread-list/', admin_unread_list, name='admin_unread_list'),
    path('api/unread-count/', customer_unread_count, name='customer_unread_count'),
] 