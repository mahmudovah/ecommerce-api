from rest_framework import serializers
from product.serializers import ProductListSerializer
from order.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductListSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status','total_amount','shipping_address','phone',
                  'notes', 'items','created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at','total_amount']


class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    phone = serializers.CharField(max_length=13)
    notes = serializers.CharField(required=False, allow_blank=True)
