from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE_CHOICES = (
        ('CUSTOMER', 'Покупатель'),
        ('ADMIN', 'Администратор'),
        ('MANAGER', 'Менеджер'),
    )

    FAVORITE_CATEGORY_CHOICES = (
        ('rings', 'Кольца'),
        ('bracelets', 'Браслеты'),
        ('pendants', 'Подвески'),
        ('earrings', 'Серьги'),
        ('necklaces', 'Ожерелья'),
    )

    # related_name='shop' — не трогаем, чтобы не ломать существующий код
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    full_name = models.CharField('ФО', max_length=150, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    address = models.TextField('Адрес доставки', blank=True, null=True)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    favorite_category = models.CharField(
        'Любимая категория украшений',
        max_length=20,
        choices=FAVORITE_CATEGORY_CHOICES,
        blank=True,
        null=True
    )
    city = models.CharField('Город доставки', max_length=100, blank=True, null=True)
    postal_code = models.CharField('Почтовый индекс', max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'myproject_profile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.username}'

    def is_admin(self):
        return self.role == 'ADMIN' or self.user.is_staff or self.user.is_superuser

    def get_role_badge_color(self):
        return {'CUSTOMER': 'success', 'MANAGER': 'warning', 'ADMIN': 'danger'}.get(self.role, 'secondary')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'ADMIN' if (instance.is_staff or instance.is_superuser) else 'CUSTOMER'
        Profile.objects.get_or_create(user=instance, defaults={'role': role})


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'shop'):
        instance.shop.save()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    opisanie = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'myproject_categorytovar'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    opisanie = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'myproject_proizvoditel'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    opisanie = models.TextField(blank=True, null=True)
    fotto = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        db_table = 'myproject_tovar'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'myproject_korzina'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'

    def get_total_price(self):
        if not self.product or self.product.price is None:
            return 0
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_address = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} — {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'