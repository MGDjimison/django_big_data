from datetime import timedelta

from django.db import models
from django.utils import timezone


class BookAuthor(models.Model):
    full_name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'book_authors'
        indexes = [
            models.Index(fields=['full_name']),
        ]


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(BookAuthor, on_delete=models.CASCADE)
    description = models.TextField()
    published_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['published_date']),
        ]


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey('users.User', on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower} - {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.return_date:
            loan_date = self.loan_date or timezone.localdate()
            self.return_date = loan_date + timedelta(days=14)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'loans'
        indexes = [
            models.Index(fields=['borrower']),
            models.Index(fields=['loan_date']),
        ]
