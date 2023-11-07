from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books_created")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn_number = models.CharField(max_length=13, null=True, blank=True)
    cover_image = models.URLField(null=True, blank=True)
    categories = models.ManyToManyField("Category", through='BookCategory', related_name="books")

    def __str__(self):
        return self.title