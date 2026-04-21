from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductCategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet)
router.register(r'products', ProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
