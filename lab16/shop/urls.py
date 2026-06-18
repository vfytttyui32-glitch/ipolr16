from django.urls import path
from . import views

urlpatterns = [
 
    path('',views.home,name='home'),
    path('about-shop/',views.shop, name='about_shop'),
    path('about-author/',views.author, name='about_author'),
]