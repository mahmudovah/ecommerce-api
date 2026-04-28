from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'User Cart: {self.user.username}'
    
    @property
    def total_items(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total
    
    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    class Meta:
        unique_together = ('cart', 'product')