from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductCategoryViewSet, ProductViewSet
from cart.views import CartViewSet
from rest_framework.authtoken.views import obtain_auth_token
from order.views import OrderViewSet

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', obtain_auth_token)
]
