# Generated by Django 4.2.17 on 2025-01-04 07:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0003_alter_review_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='likes',
        ),
        migrations.AddField(
            model_name='review',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
