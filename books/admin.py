from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Book, Genre

class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]

class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "get_genres", "created_at", "updated_at"]
    list_filter = ["created_at"]

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = "Genres"  # Column name in the admin panel


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
