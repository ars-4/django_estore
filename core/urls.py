from django.urls import path, include
from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='ProductsViewSet')
router.register('category', views.CategoryViewSet, basename='CategoryViewSet')
router.register('order', views.OrderViewSet, basename='OrderViewSet')
router.register('orderitem', views.OrderItemViewSet, basename='OrderItemViewSet')
router.register('cart', views.CartViewSet, basename='CartViewSet')
router.register('subcategory', views.SubCategoryViewSet, basename='SubCategoryViewSet')

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='LoginView'),
    path('register/', views.register, name='RegisterView'),
    
    path('api/', include(router.urls))
]
