from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return HttpResponse('Добро пожаловать в магазин  <b><p> <a href="/about-author/">Автор Лабораторной</a></p> <p> <a href="/about-shop/">Магазин</a></p></b>')
 
def about_author(request):
    return HttpResponse("Климович Матвей Сергеевич ")

def about_shop(request):
    return HttpResponse("<b>Создание и базовая настройка приложений Django</b>")

# Create your views here.
