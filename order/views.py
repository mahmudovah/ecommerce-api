from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer, OrderCreateSerializer
from cart.models import Cart
from order.telegram import send_telegram_notification


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('created_at')
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or cart.items.count() == 0:
            return Response ({"error" : "Savat bosh"}, status=400)
        
        serializer =OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            shipping_address=serializer.validated_data['shipping_address'],
            phone=serializer.validated_data['phone'],
            notes=serializer.validated_data.get('notes', '')
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()

        cart.items.all().delete()
        send_telegram_notification(order)
        return Response(OrderSerializer(order).data, status=201)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order: Order = self.get_object()

        if order.status == 'pending':
            order.status =='cancelled'
            order.save()
            return Response({
                'message': 'Order cancelled'
            }, status=200)
        
        return Response({
            'error':'You can not cancel this order!'
        }, status=400)