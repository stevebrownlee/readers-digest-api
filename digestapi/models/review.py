from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.first_name} {self.user.last_name} for {self.book.title}"