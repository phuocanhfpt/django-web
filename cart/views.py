from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse

def get_cart(request):
    if request.user.is_authenticated:
        # Xóa cart rỗng cũ
        Cart.objects.filter(user=request.user, items__isnull=True).delete()
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        # Xóa cart rỗng cũ
        Cart.objects.filter(session_id=request.session.session_key, items__isnull=True).delete()
        cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
    # Lưu cart_id vào session để context processor lấy đúng cart
    request.session['cart_id'] = cart.id
    return cart

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'Đã thêm {product.name} vào giỏ hàng.')
    return redirect('cart:cart_detail')

def cart_remove(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('cart:cart_detail')

def cart_update(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Đã cập nhật số lượng sản phẩm.')
    else:
        cart_item.delete()
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('cart:cart_detail')

def cart_api(request):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by('-created').first()
    else:
        if request.session.session_key:
            cart = Cart.objects.filter(session_id=request.session.session_key).order_by('-created').first()
    items = []
    total = 0
    total_items = 0
    if cart:
        for item in cart.items.select_related('product').all():
            product = item.product
            image_url = ''
            if hasattr(product, 'image') and product.image:
                try:
                    image_url = product.image.url
                except Exception:
                    image_url = ''
            product_url = '#'
            if hasattr(product, 'get_absolute_url'):
                try:
                    product_url = product.get_absolute_url()
                except Exception:
                    product_url = '#'
            items.append({
                'id': item.id,
                'name': product.name,
                'image': image_url,
                'price': int(product.price),
                'quantity': item.quantity,
                'total': int(item.get_cost()),
                'url': product_url
            })
            total += item.get_cost()
            total_items += item.quantity
    return JsonResponse({
        'items': items,
        'total': int(total),
        'total_items': total_items
    })
