from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

from shop.models import Profile, Order, OrderItem, Cart, CartItem
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer, OrderSerializer


# ─── helpers ───────────────────────────────────────────────────────────────────

def _is_admin(user):
    profile = getattr(user, 'shop', None)
    return (profile and profile.role == 'ADMIN') or user.is_staff or user.is_superuser


# ─── REST API ──────────────────────────────────────────────────────────────────

class RegisterView(views.APIView):
    """POST /api/auth/register/  — регистрация, доступно всем"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Аккаунт создан'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """POST /api/auth/login/  — вход через session"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Неверное имя пользователя или пароль'},
                        status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """POST /api/auth/logout/"""

    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен'})


class MeView(views.APIView):
    """
    GET  /api/auth/me/   — профиль текущего пользователя (только аутентифицированные → 401)
    PATCH /api/auth/me/  — изменение профиля
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        # related_name = 'shop', не 'profile'
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # обновляем email если передан
            if 'email' in request.data:
                request.user.email = request.data['email']
                request.user.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersView(views.APIView):
    """
    GET /api/orders/
      — покупатель видит только свои заказы
      — администратор видит все
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if _is_admin(request.user):
            orders = Order.objects.all().select_related('user').prefetch_related('items')
        else:
            orders = Order.objects.filter(user=request.user).prefetch_related('items')
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        """Создать заказ из корзины"""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Корзина не найдена'}, status=status.HTTP_400_BAD_REQUEST)

        items = cart.cartitem_set.select_related('product').all()
        if not items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        profile = getattr(request.user, 'shop', None)
        address = profile.address if profile else ''
        total = sum(i.get_total_price() for i in items)

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            shipping_address=address,
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )
        cart.cartitem_set.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# ─── HTML views ────────────────────────────────────────────────────────────────

def login_page(request):
    """Страница входа (HTML-форма, session auth)"""
    if request.user.is_authenticated:
        return redirect('profile')
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'profile'))
        error = 'Неверное имя пользователя или пароль'
    return render(request, 'accounts/login.html', {'error': error})


def register_page(request):
    """Страница регистрации (HTML-форма)"""
    if request.user.is_authenticated:
        return redirect('profile')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if password != password2:
            error = 'Пароли не совпадают'
        elif User.objects.filter(username=username).exists():
            error = 'Пользователь с таким именем уже существует'
        elif len(password) < 6:
            error = 'Пароль должен быть не менее 6 символов'
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            login(request, user)
            messages.success(request, 'Добро пожаловать! Аккаунт создан.')
            return redirect('profile')
    return render(request, 'accounts/register.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('product_list')


@login_required
def profile_view(request):
    """Личный кабинет"""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if _is_admin(request.user):
        orders = Order.objects.all().select_related('user').prefetch_related('items__product')
    else:
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'orders': orders,
        'is_admin': _is_admin(request.user),
    })


@login_required
def settings_view(request):
    """Страница настроек — смена пароля и email"""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password2 = request.POST.get('new_password2')

            if not request.user.check_password(old_password):
                messages.error(request, 'Текущий пароль введён неверно')
            elif new_password != new_password2:
                messages.error(request, 'Новые пароли не совпадают')
            elif len(new_password) < 6:
                messages.error(request, 'Пароль должен быть не менее 6 символов')
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Пароль успешно изменён')
                return redirect('settings')

        elif action == 'change_email':
            new_email = request.POST.get('email', '').strip()
            if not new_email:
                messages.error(request, 'Email не может быть пустым')
            elif User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
                messages.error(request, 'Этот email уже используется')
            else:
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Email успешно изменён')
                return redirect('settings')

    return render(request, 'accounts/settings.html', {
        'profile': profile,
        'is_admin': _is_admin(request.user),
    })