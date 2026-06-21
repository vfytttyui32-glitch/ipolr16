from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, MeView, OrdersView,
    login_page, register_page, logout_view, profile_view, settings_view,
)

urlpatterns = [
    # REST API
    path('api/auth/register/', RegisterView.as_view(), name='api_register'),
    path('api/auth/login/', LoginView.as_view(), name='api_login'),
    path('api/auth/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/auth/me/', MeView.as_view(), name='api_me'),
    path('api/orders/', OrdersView.as_view(), name='api_orders'),

    # HTML страницы
    path('accounts/login/', login_page, name='login'),
    path('accounts/register/', register_page, name='register'),
    path('accounts/logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
]