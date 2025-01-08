from django.urls import path
from .views import CreateReviewView, EditReviewView, toggle_like_review

app_name = 'reviews'

urlpatterns = [
    path('create/<int:pk>/', CreateReviewView.as_view(), name='create_review'),
    path('edit/<int:pk>/', EditReviewView.as_view(), name='edit_review'),
    path('like/<int:pk>/', toggle_like_review, name='toggle_like_review'),
]