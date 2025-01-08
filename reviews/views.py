from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from .models import Review
from books.models import Book
from django.http import JsonResponse

class CreateReviewView(CreateView):
    model = Review
    fields = ['rating', 'comment', 'spoiler_tag']
    template_name = 'reviews/review.html'

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        form.instance.book = book
        form.instance.user = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):

        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        if self.request.user.is_authenticated and Review.objects.filter(book=book, user=self.request.user).exists():
            return redirect('reviews:edit_review', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('books:detail', kwargs={'pk': self.kwargs['pk']})

class EditReviewView(UpdateView):
    model = Review
    fields = ['rating', 'comment', 'spoiler_tag']
    template_name = 'reviews/edit_review.html'

    def get_object(self, queryset=None):

        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return get_object_or_404(Review, book=book, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('books:detail', kwargs={'pk': self.kwargs['pk']})

def toggle_like_review(request, pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=pk)
        if request.user in review.likes.all():
            # User already liked, so unlike
            review.likes.remove(request.user)
            liked = False
        else:
            # User hasn't liked yet, so like
            review.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': review.total_likes()})
    return JsonResponse({'error': 'Unauthorized'}, status=401)