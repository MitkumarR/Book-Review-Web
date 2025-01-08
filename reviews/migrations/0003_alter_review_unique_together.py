# Generated by Django 4.2.17 on 2024-12-29 11:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0003_genre_remove_book_genre_book_genre"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reviews", "0002_alter_review_rating"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("user", "book")},
        ),
    ]
