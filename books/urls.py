from django.urls import path

from books.views import  IndexView, DetailView, GenreView, GenreListView
from books import models

app_name = "books"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>", DetailView.as_view(), name="detail"),
    path('genres/', GenreListView.as_view(), name='genres'),
    path('genres/<str:genre_name>/', GenreView.as_view(), name='genre'),
]