from .models import Cart

def cart(request):
    cart = None
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.prefetch_related('items').get(id=cart_id)
        except Cart.DoesNotExist:
            cart = None
    cart_items = cart.items.all() if cart else []
    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total_items': sum(item.quantity for item in cart_items),
        'cart_total_cost': cart.get_total_cost_after_discount() if cart else 0
    } 