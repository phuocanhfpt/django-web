from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Message, Conversation, ChatConfig
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from functools import wraps
import threading

def check_chat_enabled(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        config = ChatConfig.get_config()
        if not config.is_enabled:
            return JsonResponse({'error': 'Chat đã bị tắt'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.

@login_required
@check_chat_enabled
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        Q(sender_user=request.user, conversation__user=other_user) | Q(sender_user=other_user, conversation__user=request.user)
    ).order_by('timestamp')
    return render(request, 'chat/chat.html', {
        'other_user': other_user,
        'messages': messages,
    })

@staff_member_required
@check_chat_enabled
def admin_conversation_list(request):
    conversations = Conversation.objects.order_by('-last_active')
    return render(request, 'chat/admin_conversation_list.html', {
        'conversations': conversations,
    })

@staff_member_required
@check_chat_enabled
def admin_conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    return render(request, 'chat/admin_conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
    })

@check_chat_enabled
def get_or_create_conversation(request):
    if request.user.is_authenticated:
        conversation, created = Conversation.objects.get_or_create(user=request.user, is_closed=False)
        guest_name = request.user.get_full_name() or request.user.username
    else:
        guest_name = request.session.get('guest_name')
        if not guest_name:
            guest_name = request.GET.get('guest_name')
            if guest_name:
                request.session['guest_name'] = guest_name
        if not guest_name:
            return JsonResponse({'need_name': True})
        conversation, created = Conversation.objects.get_or_create(
            guest_name=guest_name, user=None, is_closed=False
        )
    return JsonResponse({'conversation_id': conversation.id, 'guest_name': guest_name})

@csrf_exempt
@check_chat_enabled
def send_message(request):
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        content = request.POST.get('content')
        if not conversation_id or not content:
            return JsonResponse({'error': 'Thiếu dữ liệu'}, status=400)
        conversation = Conversation.objects.get(id=conversation_id)
        if request.user.is_authenticated:
            sender = request.user.get_full_name() or request.user.username
            is_admin = request.user.is_staff
            sender_user = request.user
        else:
            sender = request.session.get('guest_name', 'Guest')
            is_admin = False
            sender_user = None
        msg = Message.objects.create(
            conversation=conversation,
            sender=sender,
            sender_user=sender_user,
            content=content,
            is_admin=is_admin
        )
        conversation.last_active = timezone.now()
        conversation.save()

        # --- AUTO REPLY LOGIC ---
        config = ChatConfig.get_config()
        if config.auto_reply_enabled and not is_admin:
            # Chỉ gửi auto-reply nếu chưa có tin nhắn admin nào trong cuộc trò chuyện này
            def send_auto_reply():
                # Kiểm tra lại lần nữa trước khi gửi
                if not Message.objects.filter(conversation=conversation, is_admin=True).exists():
                    Message.objects.create(
                        conversation=conversation,
                        sender="Hệ thống",
                        sender_user=None,
                        content=config.auto_reply_message or "Cảm ơn bạn đã liên hệ! Hiện tại chưa có admin trực tuyến. Chúng tôi sẽ phản hồi sớm nhất có thể.",
                        is_admin=True
                    )
            # Nếu chưa có admin trả lời, lên lịch gửi auto-reply sau delay
            if not Message.objects.filter(conversation=conversation, is_admin=True).exists():
                timer = threading.Timer(config.auto_reply_delay, send_auto_reply)
                timer.start()

        return JsonResponse({
            'id': msg.id,
            'sender': msg.sender,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M %d/%m/%Y'),
            'is_admin': msg.is_admin,
        })
    return JsonResponse({'error': 'Chỉ hỗ trợ POST'}, status=405)

@check_chat_enabled
def get_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    # Nếu là admin, đánh dấu các tin nhắn khách chưa đọc thành đã đọc
    if request.user.is_authenticated and request.user.is_staff:
        Message.objects.filter(conversation_id=conversation_id, is_admin=False, is_read=False).update(is_read=True)
    data = [{
        'id': m.id,
        'sender': m.sender,
        'content': m.content,
        'timestamp': m.timestamp.strftime('%H:%M %d/%m/%Y'),
        'is_admin': m.is_admin,
    } for m in messages]
    return JsonResponse({'messages': data})

@staff_member_required
@check_chat_enabled
def admin_unread_count(request):
    # Chỉ đếm tin nhắn chưa đọc từ khách (is_admin=False, is_read=False)
    unread = Conversation.objects.filter(
        is_closed=False,
        messages__is_admin=False,
        messages__is_read=False
    ).distinct().count()
    return JsonResponse({'unread': unread})

@staff_member_required
@check_chat_enabled
def admin_latest_unread_conversation(request):
    # Lấy conversation mới nhất có tin nhắn chưa đọc từ khách
    conv = Conversation.objects.filter(
        is_closed=False,
        messages__is_admin=False,
        messages__is_read=False
    ).distinct().order_by('-last_active').first()
    if conv:
        return JsonResponse({'conversation_id': conv.id})
    return JsonResponse({'conversation_id': None})

@staff_member_required
@check_chat_enabled
def admin_unread_list(request):
    # Lấy các conversation còn mở, có tin nhắn chưa đọc từ khách (is_admin=False, is_read=False)
    conversations = (
        Conversation.objects
        .filter(is_closed=False, messages__is_admin=False, messages__is_read=False)
        .distinct()
        .order_by('-last_active')
    )
    unread_list = []
    for conv in conversations:
        unread_count = conv.messages.filter(is_admin=False, is_read=False).count()
        if unread_count == 0:
            continue
        customer_name = conv.user.username if conv.user else conv.guest_name or f"Khách #{conv.id}"
        unread_list.append({
            'conversation_id': conv.id,
            'customer_name': customer_name,
            'unread_count': unread_count,
        })
    return JsonResponse({'unread_list': unread_list})

@check_chat_enabled
def customer_unread_count(request):
    # Lấy conversation_id từ session hoặc từ request.GET
    conversation_id = request.session.get('conversation_id') or request.GET.get('conversation_id')
    if not conversation_id:
        return JsonResponse({'unread': 0})
    
    # Kiểm tra tin nhắn chưa đọc từ admin
    unread = Message.objects.filter(
        conversation_id=conversation_id,
        is_admin=True,  # Chỉ đếm tin nhắn từ admin
        is_read=False   # Chỉ đếm tin nhắn chưa đọc
    ).count()
    
    return JsonResponse({'unread': unread})
