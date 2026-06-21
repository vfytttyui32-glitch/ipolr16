from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ValidationError

class Proizvoditel(models.Model):
    name = models.CharField(max_length=400)
    country = models.CharField(max_length=400)
    opisanie = models.TextField()

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Categorytovar(models.Model):
    name = models.CharField(max_length=400)
    opisanie = models.TextField()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tovar(models.Model):
    name = models.CharField(max_length=400)
    opisanie = models.TextField()
    fotto = models.ImageField()
    cena = models.DecimalField(max_digits=30, decimal_places=3)
    colnasklade = models.IntegerField()
    category = models.ForeignKey(Categorytovar, on_delete=models.CASCADE, related_name='Tovars')
    prozvoditel = models.ForeignKey(Proizvoditel, on_delete=models.CASCADE, related_name='prozvol')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Korzina(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_cost(self):
        total = Decimal('0.00')
        for item in self.items.select_related('product').all():
            total += item.item_cost()
        return total


class KorzinaItem(models.Model):
    cart = models.ForeignKey(
        Korzina,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Tovar,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'

    def clean(self):
        if self.quantity > self.product.colnasklade:
            raise ValidationError("Количество превышает доступное на складе")

    def стоимость_элемента(self):
        return self.product.cena * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"