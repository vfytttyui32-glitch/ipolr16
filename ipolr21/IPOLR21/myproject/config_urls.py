"""
Корневые URL-маршруты проекта.
Задание 4: подключение системы аутентификации Django.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Административная панель (Задание 5)
    path("admin/", admin.site.urls),

    # Задание 4: аутентификация Django
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="shop/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/catalog/"), name="logout"),

    # Приложение shop (Задание 1)
    path("", include("shop.urls")),
]

# Раздача медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)