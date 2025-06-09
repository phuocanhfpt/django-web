from django.db.models import Count, Q
from .models import Category

def cart_count(request):
    from cart.models import Cart, CartItem
    count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        if not request.session.session_key:
            request.session.create()
        cart = Cart.objects.filter(session_id=request.session.session_key).first()
    if cart:
        count = sum(item.quantity for item in cart.items.all())
    return {'cart_count': count}

def product_categories(request):
    return {
        'product_categories': Category.objects.filter(status='active')
            .annotate(product_count=Count('products', filter=Q(products__status=True)))
    } 