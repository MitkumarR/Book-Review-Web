from django.contrib import messages
from django.views.generic import TemplateView, ListView
from books.models import Book, Genre
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = "home.html"  # Point to your template file

class BookSearchView(ListView):
    model = Book
    template_name = "search_results.html"
    context_object_name = "books"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(title__icontains=query)  # Case-insensitive search
        return Book.objects.none()

class ExploreView(TemplateView):
    template_name = "explore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_books'] = Book.objects.order_by('-created_at')[:5]  # Fetch 10 most recent books
        context['genres'] = Genre.objects.all()[:5]
        context['books_by_genre'] = {genre: Book.objects.filter(genre=genre)[:5] for genre in context['genres']}
        return context

def my_view(request):
    messages.success(request, "Your action was successful!")
    messages.error(request, "Something went wrong.")
    return render(request, 'your_template.html')