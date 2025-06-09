from django.db import models
from django.conf import settings
from products.models import Product, Promotion
from decimal import Decimal

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    promotion = models.ForeignKey(Promotion, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Cart {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        if self.promotion and self.promotion.status:
            total = self.get_total_cost()
            if self.promotion.type == 'percentage':
                discount = total * Decimal(self.promotion.discount) / 100
                if self.promotion.max_discount:
                    discount = min(discount, self.promotion.max_discount)
            else:  # fixed
                discount = Decimal(self.promotion.discount)
            # Kiểm tra min_purchase
            if self.promotion.min_purchase and total < self.promotion.min_purchase:
                return Decimal('0')
            return discount
        return Decimal('0')

    def get_total_cost_after_discount(self):
        return max(self.get_total_cost() - self.get_discount(), 0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.price * self.quantity
