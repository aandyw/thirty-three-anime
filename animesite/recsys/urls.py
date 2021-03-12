from django.urls import path

from . import views

urlpatterns = [
    path('', views.anime_view, name='anime view'),
]
