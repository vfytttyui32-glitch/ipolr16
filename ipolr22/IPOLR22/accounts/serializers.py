from rest_framework import serializers
from django.contrib.auth.models import User
from shop.models import Profile, Order, OrderItem


class ProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    role_badge = serializers.CharField(source='get_role_badge_color', read_only=True)
    favorite_category_display = serializers.CharField(
        source='get_favorite_category_display', read_only=True
    )

    class Meta:
        model = Profile
        fields = [
            'full_name', 'phone', 'address', 'role', 'role_display', 'role_badge',
            'favorite_category', 'favorite_category_display', 'city', 'postal_code'
        ]
        # role нельзя менять через PATCH самому себе — только через admin
        read_only_fields = ['role', 'role_display', 'role_badge']


class UserSerializer(serializers.ModelSerializer):
    # related_name в модели — 'shop', поэтому source='shop'
    profile = ProfileSerializer(source='shop', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(
        source='subtotal', max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'username', 'status', 'status_display',
            'total_amount', 'shipping_address', 'created_at', 'items'
        ]