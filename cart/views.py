from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from product.models import Product


class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    def list(self, request):
        cart =self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({
                'error': 'Product is not available'
            }, status=404)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={
                'quantity': quantity
            }
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        cart = self.get_object()
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'}, status=204)
    
    @action(detail=False, methods=['patch'])
    def update_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity',1)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({
                'error': 'Item is not available'
            }, status=404)
        
        if quantity > cart_item.product.stock:
            return Response({'message': f'Mahsulot yetarli emas. Qoldi: {cart_item.product.stock}'}, status=400)

        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)