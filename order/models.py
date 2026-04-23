from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('shipped', 'Yetkazilmoqda'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    user: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    total_amount = models.IntegerField(default=0)
    shipping_address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    

class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product: Product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField(default=0)  # buyurtma vaqtidagi narx

    @property
    def total_price(self):
        return self.price * self.quantity