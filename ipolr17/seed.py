import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from ipolr17.Ipolr17.IPOLR17.myproject.models import Proizvoditel, Categorytovar, Tovar, Korzina, KorzinaItem

# ========== ПРОИЗВОДИТЕЛИ (5 шт.) ==========
manufacturers_data = [
    {'name': 'Мастерская Ганны', 'country': 'Беларусь', 'opisanie': 'Изделия ручной работы из натуральных материалов'},
    {'name': 'HandCraft BY', 'country': 'Беларусь', 'opisanie': 'Авторские украшения и аксессуары'},
    {'name': 'Вязаный мир', 'country': 'Беларусь', 'opisanie': 'Вязаные изделия на заказ'},
    {'name': 'Деревянные чудеса', 'country': 'Беларусь', 'opisanie': 'Изделия из дерева ручной работы'},
    {'name': 'Студия Натальи', 'country': 'Беларусь', 'opisanie': 'Украшения из полимерной глины и смолы'},
]

manufacturers = []
for m in manufacturers_data:
    obj, _ = Proizvoditel.objects.get_or_create(name=m['name'], defaults=m)
    manufacturers.append(obj)
print(f'✅ Производители: {len(manufacturers)} шт.')

# ========== КАТЕГОРИИ (10 шт.) ==========
categories_data = [
    {'name': 'Украшения', 'opisanie': 'Браслеты, кольца, серьги ручной работы'},
    {'name': 'Вязаные изделия', 'opisanie': 'Шапки, шарфы, свитера'},
    {'name': 'Игрушки', 'opisanie': 'Мягкие игрушки и амигуруми'},
    {'name': 'Деревянные изделия', 'opisanie': 'Разделочные доски, статуэтки, рамки'},
    {'name': 'Свечи и мыло', 'opisanie': 'Аромасвечи и натуральное мыло'},
    {'name': 'Картины и постеры', 'opisanie': 'Живопись и графика'},
    {'name': 'Сумки и кошельки', 'opisanie': 'Изделия из кожи и ткани'},
    {'name': 'Посуда', 'opisanie': 'Керамика и расписная посуда'},
    {'name': 'Открытки', 'opisanie': 'Авторские открытки и скрапбукинг'},
    {'name': 'Одежда', 'opisanie': 'Авторская одежда и аксессуары'},
]

categories = []
for c in categories_data:
    obj, _ = Categorytovar.objects.get_or_create(name=c['name'], defaults=c)
    categories.append(obj)
print(f'✅ Категории: {len(categories)} шт.')

# ========== ТОВАРЫ (34 шт.) ==========
products_data = [
    # Украшения
    {'name': 'Браслет из бисера "Лето"', 'cena': 12.500, 'colnasklade': 15, 'category': categories[0], 'prozvoditel': manufacturers[1], 'opisanie': 'Яркий браслет ручной работы из чешского бисера'},
    {'name': 'Серьги "Лесная фея"', 'cena': 18.000, 'colnasklade': 10, 'category': categories[0], 'prozvoditel': manufacturers[4], 'opisanie': 'Серьги из полимерной глины с цветочным узором'},
    {'name': 'Кольцо из смолы с цветком', 'cena': 9.900, 'colnasklade': 20, 'category': categories[0], 'prozvoditel': manufacturers[4], 'opisanie': 'Кольцо из эпоксидной смолы с настоящим цветком внутри'},
    {'name': 'Колье "Минимализм"', 'cena': 22.000, 'colnasklade': 8, 'category': categories[0], 'prozvoditel': manufacturers[1], 'opisanie': 'Лаконичное колье из серебряной проволоки'},
    # Вязаные изделия
    {'name': 'Шапка вязаная "Зима"', 'cena': 25.000, 'colnasklade': 12, 'category': categories[1], 'prozvoditel': manufacturers[2], 'opisanie': 'Тёплая шапка из мериносовой шерсти'},
    {'name': 'Шарф "Скандинавия"', 'cena': 30.000, 'colnasklade': 7, 'category': categories[1], 'prozvoditel': manufacturers[2], 'opisanie': 'Длинный шарф со скандинавским узором'},
    {'name': 'Носки шерстяные', 'cena': 14.000, 'colnasklade': 25, 'category': categories[1], 'prozvoditel': manufacturers[2], 'opisanie': 'Тёплые носки из натуральной шерсти'},
    {'name': 'Плед вязаный "Уют"', 'cena': 85.000, 'colnasklade': 3, 'category': categories[1], 'prozvoditel': manufacturers[2], 'opisanie': 'Большой плед крупной вязки'},
    # Игрушки
    {'name': 'Зайчик амигуруми', 'cena': 16.000, 'colnasklade': 18, 'category': categories[2], 'prozvoditel': manufacturers[0], 'opisanie': 'Вязаный зайчик ручной работы'},
    {'name': 'Медвежонок Тедди', 'cena': 20.000, 'colnasklade': 10, 'category': categories[2], 'prozvoditel': manufacturers[0], 'opisanie': 'Мягкая игрушка из гипоаллергенных материалов'},
    {'name': 'Кукла текстильная', 'cena': 35.000, 'colnasklade': 5, 'category': categories[2], 'prozvoditel': manufacturers[0], 'opisanie': 'Авторская текстильная кукла'},
    {'name': 'Лисёнок из фетра', 'cena': 13.000, 'colnasklade': 14, 'category': categories[2], 'prozvoditel': manufacturers[0], 'opisanie': 'Мягкая игрушка из фетра'},
    # Деревянные изделия
    {'name': 'Разделочная доска "Сердце"', 'cena': 28.000, 'colnasklade': 9, 'category': categories[3], 'prozvoditel': manufacturers[3], 'opisanie': 'Доска из дуба в форме сердца'},
    {'name': 'Рамка для фото деревянная', 'cena': 19.000, 'colnasklade': 11, 'category': categories[3], 'prozvoditel': manufacturers[3], 'opisanie': 'Рамка ручной работы с резьбой'},
    {'name': 'Статуэтка "Сова"', 'cena': 24.000, 'colnasklade': 6, 'category': categories[3], 'prozvoditel': manufacturers[3], 'opisanie': 'Резная сова из липы'},
    {'name': 'Подставка под телефон', 'cena': 15.000, 'colnasklade': 20, 'category': categories[3], 'prozvoditel': manufacturers[3], 'opisanie': 'Деревянная подставка с гравировкой'},
    # Свечи и мыло
    {'name': 'Свеча ароматическая "Ваниль"', 'cena': 11.000, 'colnasklade': 30, 'category': categories[4], 'prozvoditel': manufacturers[0], 'opisanie': 'Соевая свеча с ароматом ванили'},
    {'name': 'Мыло "Лаванда"', 'cena': 7.500, 'colnasklade': 40, 'category': categories[4], 'prozvoditel': manufacturers[0], 'opisanie': 'Натуральное мыло с лавандовым маслом'},
    {'name': 'Набор свечей "Уют"', 'cena': 32.000, 'colnasklade': 8, 'category': categories[4], 'prozvoditel': manufacturers[0], 'opisanie': 'Набор из 3 ароматических свечей'},
    # Картины
    {'name': 'Картина "Закат"', 'cena': 55.000, 'colnasklade': 2, 'category': categories[5], 'prozvoditel': manufacturers[4], 'opisanie': 'Акварель, 30х40 см'},
    {'name': 'Постер "Минск"', 'cena': 18.000, 'colnasklade': 15, 'category': categories[5], 'prozvoditel': manufacturers[4], 'opisanie': 'Авторский постер с видами Минска'},
    # Сумки
    {'name': 'Сумка-шоппер льняная', 'cena': 22.000, 'colnasklade': 12, 'category': categories[6], 'prozvoditel': manufacturers[1], 'opisanie': 'Экологичная сумка из льна'},
    {'name': 'Кошелёк кожаный', 'cena': 45.000, 'colnasklade': 7, 'category': categories[6], 'prozvoditel': manufacturers[1], 'opisanie': 'Кошелёк из натуральной кожи'},
    {'name': 'Косметичка вязаная', 'cena': 17.000, 'colnasklade': 10, 'category': categories[6], 'prozvoditel': manufacturers[2], 'opisanie': 'Вязаная косметичка с подкладкой'},
    # Посуда
    {'name': 'Кружка керамическая "Лес"', 'cena': 21.000, 'colnasklade': 14, 'category': categories[7], 'prozvoditel': manufacturers[0], 'opisanie': 'Керамическая кружка с лесным рисунком'},
    {'name': 'Тарелка расписная', 'cena': 34.000, 'colnasklade': 6, 'category': categories[7], 'prozvoditel': manufacturers[0], 'opisanie': 'Тарелка с ручной росписью'},
    {'name': 'Набор пиал', 'cena': 48.000, 'colnasklade': 5, 'category': categories[7], 'prozvoditel': manufacturers[0], 'opisanie': 'Набор из 4 керамических пиал'},
    # Открытки
    {'name': 'Открытка "С днём рождения"', 'cena': 4.500, 'colnasklade': 50, 'category': categories[8], 'prozvoditel': manufacturers[4], 'opisanie': 'Авторская открытка ручной работы'},
    {'name': 'Открытка "Новый год"', 'cena': 5.000, 'colnasklade': 45, 'category': categories[8], 'prozvoditel': manufacturers[4], 'opisanie': 'Новогодняя открытка с конвертом'},
    {'name': 'Набор открыток "Цветы"', 'cena': 12.000, 'colnasklade': 20, 'category': categories[8], 'prozvoditel': manufacturers[4], 'opisanie': 'Набор из 5 открыток с цветами'},
    # Одежда
    {'name': 'Повязка на голову вязаная', 'cena': 10.000, 'colnasklade': 22, 'category': categories[9], 'prozvoditel': manufacturers[2], 'opisanie': 'Мягкая повязка из хлопка'},
    {'name': 'Варежки "Снежинка"', 'cena': 19.000, 'colnasklade': 16, 'category': categories[9], 'prozvoditel': manufacturers[2], 'opisanie': 'Вязаные варежки со снежинкой'},
    {'name': 'Топ вязаный летний', 'cena': 38.000, 'colnasklade': 8, 'category': categories[9], 'prozvoditel': manufacturers[2], 'opisanie': 'Лёгкий вязаный топ из хлопка'},
    {'name': 'Берет "Осень"', 'cena': 27.000, 'colnasklade': 11, 'category': categories[9], 'prozvoditel': manufacturers[2], 'opisanie': 'Стильный берет из шерсти'},
]

products = []
for p in products_data:
    obj, _ = Tovar.objects.get_or_create(name=p['name'], defaults=p)
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

    cart, _ = Korzina.objects.get_or_create(user=user)
    for product, qty in cart_items_per_user[i]:
        KorzinaItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': qty})

print(f'✅ Пользователи: 5 шт. (пароль для всех: password123)')
print(f'✅ Корзины созданы для каждого пользователя')
print()
print('🎉 База данных успешно заполнена!')