import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import Category, Manufacturer, Product, Cart, CartItem

# ========== ПРОИЗВОДИТЕЛИ (5 шт.) ==========
manufacturers_data = [
    {'name': 'Мастерская Ганны', 'country': 'Беларусь'},
    {'name': 'HandCraft BY', 'country': 'Беларусь'},
    {'name': 'Вязаный мир', 'country': 'Беларусь'},
    {'name': 'Деревянные чудеса', 'country': 'Беларусь'},
    {'name': 'Студия Натальи', 'country': 'Беларусь'},
]

manufacturers = []
for m in manufacturers_data:
    obj, _ = Manufacturer.objects.get_or_create(name=m['name'], defaults=m)
    manufacturers.append(obj)
print(f'✅ Производители: {len(manufacturers)} шт.')

# ========== КАТЕГОРИИ (10 шт.) ==========
categories_data = [
    {'name': 'Украшения', 'slug': 'ukrasheniya'},
    {'name': 'Вязаные изделия', 'slug': 'vyazanye'},
    {'name': 'Игрушки', 'slug': 'igrushki'},
    {'name': 'Деревянные изделия', 'slug': 'derevo'},
    {'name': 'Свечи и мыло', 'slug': 'svechi-mylo'},
    {'name': 'Картины и постеры', 'slug': 'kartiny'},
    {'name': 'Сумки и кошельки', 'slug': 'sumki'},
    {'name': 'Посуда', 'slug': 'posuda'},
    {'name': 'Открытки', 'slug': 'otkrytki'},
    {'name': 'Одежда', 'slug': 'odezhda'},
]

categories = []
for c in categories_data:
    obj, _ = Category.objects.get_or_create(slug=c['slug'], defaults=c)
    categories.append(obj)
print(f'✅ Категории: {len(categories)} шт.')

# ========== ТОВАРЫ (34 шт.) ==========
products_data = [
    # Украшения
    {'name': 'Браслет из бисера "Лето"', 'price': 12.50, 'quantity_in_stock': 15, 'category': categories[0], 'manufacturer': manufacturers[1], 'description': 'Яркий браслет ручной работы из чешского бисера'},
    {'name': 'Серьги "Лесная фея"', 'price': 18.00, 'quantity_in_stock': 10, 'category': categories[0], 'manufacturer': manufacturers[4], 'description': 'Серьги из полимерной глины с цветочным узором'},
    {'name': 'Кольцо из смолы с цветком', 'price': 9.90, 'quantity_in_stock': 20, 'category': categories[0], 'manufacturer': manufacturers[4], 'description': 'Кольцо из эпоксидной смолы с настоящим цветком внутри'},
    {'name': 'Колье "Минимализм"', 'price': 22.00, 'quantity_in_stock': 8, 'category': categories[0], 'manufacturer': manufacturers[1], 'description': 'Лаконичное колье из серебряной проволоки'},
    # Вязаные изделия
    {'name': 'Шапка вязаная "Зима"', 'price': 25.00, 'quantity_in_stock': 12, 'category': categories[1], 'manufacturer': manufacturers[2], 'description': 'Тёплая шапка из мериносовой шерсти'},
    {'name': 'Шарф "Скандинавия"', 'price': 30.00, 'quantity_in_stock': 7, 'category': categories[1], 'manufacturer': manufacturers[2], 'description': 'Длинный шарф со скандинавским узором'},
    {'name': 'Носки шерстяные', 'price': 14.00, 'quantity_in_stock': 25, 'category': categories[1], 'manufacturer': manufacturers[2], 'description': 'Тёплые носки из натуральной шерсти'},
    {'name': 'Плед вязаный "Уют"', 'price': 85.00, 'quantity_in_stock': 3, 'category': categories[1], 'manufacturer': manufacturers[2], 'description': 'Большой плед крупной вязки'},
    # Игрушки
    {'name': 'Зайчик амигуруми', 'price': 16.00, 'quantity_in_stock': 18, 'category': categories[2], 'manufacturer': manufacturers[0], 'description': 'Вязаный зайчик ручной работы'},
    {'name': 'Медвежонок Тедди', 'price': 20.00, 'quantity_in_stock': 10, 'category': categories[2], 'manufacturer': manufacturers[0], 'description': 'Мягкая игрушка из гипоаллергенных материалов'},
    {'name': 'Кукла текстильная', 'price': 35.00, 'quantity_in_stock': 5, 'category': categories[2], 'manufacturer': manufacturers[0], 'description': 'Авторская текстильная кукла'},
    {'name': 'Лисёнок из фетра', 'price': 13.00, 'quantity_in_stock': 14, 'category': categories[2], 'manufacturer': manufacturers[0], 'description': 'Мягкая игрушка из фетра'},
    # Деревянные изделия
    {'name': 'Разделочная доска "Сердце"', 'price': 28.00, 'quantity_in_stock': 9, 'category': categories[3], 'manufacturer': manufacturers[3], 'description': 'Доска из дуба в форме сердца'},
    {'name': 'Рамка для фото деревянная', 'price': 19.00, 'quantity_in_stock': 11, 'category': categories[3], 'manufacturer': manufacturers[3], 'description': 'Рамка ручной работы с резьбой'},
    {'name': 'Статуэтка "Сова"', 'price': 24.00, 'quantity_in_stock': 6, 'category': categories[3], 'manufacturer': manufacturers[3], 'description': 'Резная сова из липы'},
    {'name': 'Подставка под телефон', 'price': 15.00, 'quantity_in_stock': 20, 'category': categories[3], 'manufacturer': manufacturers[3], 'description': 'Деревянная подставка с гравировкой'},
    # Свечи и мыло
    {'name': 'Свеча ароматическая "Ваниль"', 'price': 11.00, 'quantity_in_stock': 30, 'category': categories[4], 'manufacturer': manufacturers[0], 'description': 'Соевая свеча с ароматом ванили'},
    {'name': 'Мыло "Лаванда"', 'price': 7.50, 'quantity_in_stock': 40, 'category': categories[4], 'manufacturer': manufacturers[0], 'description': 'Натуральное мыло с лавандовым маслом'},
    {'name': 'Набор свечей "Уют"', 'price': 32.00, 'quantity_in_stock': 8, 'category': categories[4], 'manufacturer': manufacturers[0], 'description': 'Набор из 3 ароматических свечей'},
    # Картины
    {'name': 'Картина "Закат"', 'price': 55.00, 'quantity_in_stock': 2, 'category': categories[5], 'manufacturer': manufacturers[4], 'description': 'Акварель, 30х40 см'},
    {'name': 'Постер "Минск"', 'price': 18.00, 'quantity_in_stock': 15, 'category': categories[5], 'manufacturer': manufacturers[4], 'description': 'Авторский постер с видами Минска'},
    # Сумки
    {'name': 'Сумка-шоппер льняная', 'price': 22.00, 'quantity_in_stock': 12, 'category': categories[6], 'manufacturer': manufacturers[1], 'description': 'Экологичная сумка из льна'},
    {'name': 'Кошелёк кожаный', 'price': 45.00, 'quantity_in_stock': 7, 'category': categories[6], 'manufacturer': manufacturers[1], 'description': 'Кошелёк из натуральной кожи'},
    {'name': 'Косметичка вязаная', 'price': 17.00, 'quantity_in_stock': 10, 'category': categories[6], 'manufacturer': manufacturers[2], 'description': 'Вязаная косметичка с подкладкой'},
    # Посуда
    {'name': 'Кружка керамическая "Лес"', 'price': 21.00, 'quantity_in_stock': 14, 'category': categories[7], 'manufacturer': manufacturers[0], 'description': 'Керамическая кружка с лесным рисунком'},
    {'name': 'Тарелка расписная', 'price': 34.00, 'quantity_in_stock': 6, 'category': categories[7], 'manufacturer': manufacturers[0], 'description': 'Тарелка с ручной росписью'},
    {'name': 'Набор пиал', 'price': 48.00, 'quantity_in_stock': 5, 'category': categories[7], 'manufacturer': manufacturers[0], 'description': 'Набор из 4 керамических пиал'},
    # Открытки
    {'name': 'Открытка "С днём рождения"', 'price': 4.50, 'quantity_in_stock': 50, 'category': categories[8], 'manufacturer': manufacturers[4], 'description': 'Авторская открытка ручной работы'},
    {'name': 'Открытка "Новый год"', 'price': 5.00, 'quantity_in_stock': 45, 'category': categories[8], 'manufacturer': manufacturers[4], 'description': 'Новогодняя открытка с конвертом'},
    {'name': 'Набор открыток "Цветы"', 'price': 12.00, 'quantity_in_stock': 20, 'category': categories[8], 'manufacturer': manufacturers[4], 'description': 'Набор из 5 открыток с цветами'},
    # Одежда
    {'name': 'Повязка на голову вязаная', 'price': 10.00, 'quantity_in_stock': 22, 'category': categories[9], 'manufacturer': manufacturers[2], 'description': 'Мягкая повязка из хлопка'},
    {'name': 'Варежки "Снежинка"', 'price': 19.00, 'quantity_in_stock': 16, 'category': categories[9], 'manufacturer': manufacturers[2], 'description': 'Вязаные варежки со снежинкой'},
    {'name': 'Топ вязаный летний', 'price': 38.00, 'quantity_in_stock': 8, 'category': categories[9], 'manufacturer': manufacturers[2], 'description': 'Лёгкий вязаный топ из хлопка'},
    {'name': 'Берет "Осень"', 'price': 27.00, 'quantity_in_stock': 11, 'category': categories[9], 'manufacturer': manufacturers[2], 'description': 'Стильный берет из шерсти'},
]

products = []
for p in products_data:
    obj, _ = Product.objects.get_or_create(name=p['name'], defaults=p)
    products.append(obj)
print(f'✅ Товары: {len(products)} шт.')

# ========== ПОЛЬЗОВАТЕЛИ (5 шт.) + КОРЗИНЫ ==========
users_data = [
    {'username': 'anna_ivanova', 'email': 'anna@example.com', 'first_name': 'Анна', 'last_name': 'Иванова'},
    {'username': 'petr_sidorov', 'email': 'petr@example.com', 'first_name': 'Пётр', 'last_name': 'Сидоров'},
    {'username': 'maria_koval', 'email': 'maria@example.com', 'first_name': 'Мария', 'last_name': 'Коваль'},
    {'username': 'igor_novak', 'email': 'igor@example.com', 'first_name': 'Игорь', 'last_name': 'Новак'},
    {'username': 'olga_sobol', 'email': 'olga@example.com', 'first_name': 'Ольга', 'last_name': 'Соболь'},
]

cart_items_per_user = [
    [(products[0], 2), (products[4], 1)],
    [(products[8], 1), (products[16], 3)],
    [(products[12], 1), (products[24], 2)],
    [(products[1], 2), (products[27], 4)],
    [(products[20], 1), (products[22], 1)],
]

for i, u in enumerate(users_data):
    user, created = User.objects.get_or_create(username=u['username'], defaults={
        'email': u['email'],
        'first_name': u['first_name'],
        'last_name': u['last_name'],
    })
    if created:
        user.set_password('password123')
        user.save()

    cart, _ = Cart.objects.get_or_create(user=user)
    for product, qty in cart_items_per_user[i]:
        CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': qty})

print(f'✅ Пользователи: 5 шт. (пароль для всех: password123)')
print(f'✅ Корзины созданы для каждого пользователя')
print()
print('🎉 База данных успешно заполнена!')