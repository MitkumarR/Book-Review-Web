from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'user', 'book', 'total_likes', 'spoiler_tag', 'review_date')
    search_fields = ('user__username', 'book__title', 'review_date')
    list_filter = ('rating', 'book', 'user')

    def total_likes(self, obj):
        return obj.likes.count()

    total_likes.short_description = 'Total Likes'