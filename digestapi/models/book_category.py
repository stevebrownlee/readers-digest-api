from django.db import models

class BookCategory(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    assigned_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['book', 'category']