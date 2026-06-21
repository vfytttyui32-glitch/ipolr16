from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'products', views.ProductViewSet, basename='api-products')
router.register(r'categories', views.CategoryViewSet, basename='api-categories')
router.register(r'manufacturers', views.ManufacturerViewSet, basename='api-manufacturers')
router.register(r'cart', views.CartViewSet, basename='api-cart')
router.register(r'cartitems', views.CartItemViewSet, basename='api-cartitems')

urlpatterns = [

    path('', views.index, name='product_list'),   
    path('catalog/', views.product_list, name='catalog'), 
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),

    path('api/', include(router.urls)),
]