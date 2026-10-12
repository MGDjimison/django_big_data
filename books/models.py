from django.db import models


class BookAuthor(models.Model):
    full_name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'book_authors'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(BookAuthor, on_delete=models.CASCADE)
    description = models.TextField()
    published_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'