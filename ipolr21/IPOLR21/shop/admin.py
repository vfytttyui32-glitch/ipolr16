from django.contrib import admin
from .models import Category, Manufacturer, Product, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Задание 5: CRUD через интерфейс администратора
    list_display = ("name", "category", "manufacturer", "price", "quantity_in_stock", "created_at")
    list_filter = ("category", "manufacturer")
    search_fields = ("name", "description")
    list_editable = ("price", "quantity_in_stock")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Основная информация", {"fields": ("name", "description", "image")}),
        ("Классификация", {"fields": ("category", "manufacturer")}),
        ("Цена и склад", {"fields": ("price", "quantity_in_stock")}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("product", "quantity")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "get_total_price")
    inlines = [CartItemInline]

    @admin.display(description="Сумма корзины")
    def get_total_price(self, obj):
        return f"{obj.get_total_price()} ₽"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "get_total_price")
    list_filter = ("cart__user",)

    @admin.display(description="Стоимость позиции")
    def get_total_price(self, obj):
        return f"{obj.get_total_price()} ₽"