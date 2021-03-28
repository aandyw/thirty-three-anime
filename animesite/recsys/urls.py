from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('animes', views.animes, name='animes'),
    path('fav', views.fav, name='favourite')
]
