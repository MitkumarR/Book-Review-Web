import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    LANGUAGES = [
        ('ENG', 'English'),
        ('GUJ', 'Gujarati'),
        ('HIN', 'Hindi'),
        ('SAN', 'Sanskrit'),
        ('URD', 'Urdu'),
        ('FRE', 'French'),
        ('GER', 'German'),
        ('SPA', 'Spanish'),
        ('RUS', 'Russian'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.DateField()
    pages = models.IntegerField()
    language = models.CharField(max_length=3, choices=LANGUAGES)
    thumbnail = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField()
    publisher = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 2)
        return None

    def total_reviews(self):
        return self.reviews.count()


    def __str__(self):
        return self.title

    # def was_created_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.created_at <= now
