import csv
import random
import datetime

from django.core.management.base import BaseCommand
from books.models import Book, Genre  # replace 'books' with your app name

class Command(BaseCommand):
    help = 'Import books from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        LANGUAGES = ['ENG', 'GUJ', 'HIN', 'SAN', 'URD', 'FRE', 'GER', 'SPA', 'RUS']
        PAGES_RANGE = (100, 1000)

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                isbn = row['isbn10'].strip()
                title = row['title'].strip()
                subtitle = row['subtitle'].strip() if row['subtitle'] else None
                author = row['authors'].strip()
                categories = row['categories'].split(',') if row['categories'] else []
                thumbnail = row['thumbnail'].strip() if row['thumbnail'] else None
                description = row['description'].strip()
                published_year = row['published_year'].strip()

                try:
                    publication_date = datetime.date(int(published_year), 1, 1)
                except:
                    publication_date = datetime.date(2000, 1, 1)

                language = random.choice(LANGUAGES)
                pages = random.randint(*PAGES_RANGE)

                book, created = Book.objects.get_or_create(
                    isbn=isbn,
                    defaults={
                        'title': title,
                        'subtitle': subtitle,
                        'author': author,
                        'thumbnail': thumbnail,
                        'description': description,
                        'publication_year': publication_date,
                        'pages': pages,
                        'language': language,
                        'publisher': 'NA',
                    }
                )

                for cat in categories:
                    genre_name = cat.strip()
                    if genre_name:
                        genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                        book.genre.add(genre_obj)

                book.save()
                self.stdout.write(self.style.SUCCESS(f"Imported: {book.title} ({isbn})"))
