from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from sqlalchemy.sql.sqltypes import NullType

from books.models import Book

class Review(models.Model):
    review_date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(
        default=NullType,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    comment = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reviews"
    )
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_reviews", blank=True)
    spoiler_tag = models.BooleanField(default=False)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title} - Rating: {self.rating}"
