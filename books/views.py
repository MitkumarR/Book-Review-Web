# Create your views here.
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import Book, Genre
from reviews.models import Review

class IndexView(ListView):

    template_name = "books/index.html"
    context_object_name = "book_list"

    def get_queryset(self):
        return Book.objects.order_by("-created_at")

class DetailView(DetailView):

    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context["average_rating"] = book.average_rating()
        context["total_reviews"] = book.total_reviews()
        context["reviews"] = Review.objects.filter(book=book)

        user_review = None
        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(user=self.request.user).first()

        context["user_review"] = user_review

        return context

class GenreView(ListView):
    model = Book
    template_name = "books/genre.html"
    context_object_name = "books"

    def get_queryset(self):
        genre_name = self.kwargs.get('genre_name')
        genre = get_object_or_404(Genre, name__iexact=genre_name)  # Case-insensitive lookup
        return Book.objects.filter(genre=genre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = get_object_or_404(Genre, name__iexact=self.kwargs.get('genre_name'))  # Case-insensitive
        return context

class GenreListView(ListView):
    model = Genre
    template_name = "books/genres.html"
    context_object_name = "genres"