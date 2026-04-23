from rest_framework import serializers
from product.serializers import ProductListSerializer
from cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductListSerializer(source='product', read_only=True)
    total_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id','items','total_items','total_price','created_at', 'updated_at']