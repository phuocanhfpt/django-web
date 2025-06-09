from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from products.models import Promotion
from django.utils import timezone
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Giỏ hàng trống.'})
        messages.warning(request, 'Giỏ hàng của bạn đang trống.')
        return redirect('cart:cart_detail')

    message = None
    # Xử lý AJAX apply_coupon
    if request.method == 'POST' and 'apply_coupon' in request.POST:
        code = request.POST.get('coupon_code', '').strip()
        now = timezone.now().date()
        try:
            promo = Promotion.objects.get(
                code__iexact=code,
                status=True,
                start_date__lte=now,
                end_date__gte=now
            )
            cart.promotion = promo
            cart.save()
            total_cost = f'{cart.get_total_cost_after_discount():,.0f}đ'
            return JsonResponse({'success': True, 'total_cost': total_cost})
        except Promotion.DoesNotExist:
            cart.promotion = None
            cart.save()
            return JsonResponse({'success': False, 'error': 'Mã giảm giá không hợp lệ hoặc đã hết hạn.'})

    if request.method == 'POST' and 'apply_coupon' not in request.POST:
        # Tạo đơn hàng mới
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            note=request.POST.get('note', ''),
            total_cost=cart.get_total_cost_after_discount(),
            payment_method=request.POST.get('payment_method', 'cod')
        )

        # Tạo các mục đơn hàng từ giỏ hàng
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        # Gửi email xác nhận đơn hàng cho khách
        subject = f"[Lắp Camera HCM] Xác nhận đơn hàng #{order.id}"
        to_email = order.email
        context = {
            'order': order,
            'order_items': order.items.all(),
            'site_name': 'Lắp Camera HCM',
            'site_url': 'https://lapcamerahcm.vn',
        }
        message = render_to_string('orders/order_confirmation_email.html', context)
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            html_message=message
        )

        # Xóa giỏ hàng
        cart.delete()

        messages.success(request, 'Đơn hàng của bạn đã được tạo thành công!')
        return redirect('accounts:order_detail', order_id=order.id)

    # Lấy thông tin user để tự động điền vào form
    user_info = {}
    if hasattr(request.user, 'userprofile'):
        user_info['full_name'] = request.user.userprofile.full_name or request.user.get_full_name() or request.user.username
        user_info['phone'] = request.user.userprofile.phone or ''
    else:
        user_info['full_name'] = request.user.get_full_name() or request.user.username
        user_info['phone'] = ''
    user_info['email'] = request.user.email or ''
    # Nếu có đơn hàng trước đó thì lấy địa chỉ, thành phố gần nhất
    last_order = Order.objects.filter(user=request.user).order_by('-created').first()
    if last_order:
        user_info['address'] = last_order.address
        user_info['city'] = last_order.city
    else:
        user_info['address'] = ''
        user_info['city'] = ''
    return render(request, 'orders/checkout.html', {'cart': cart, 'user_info': user_info})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order
    })
