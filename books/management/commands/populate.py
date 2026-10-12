from django.core.management.base import BaseCommand
from books.models import Book, BookAuthor
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument("object", type=str, help="The object to populate (book or author)")

    def handle(self, *args, **kwargs):
        if kwargs["object"] == "author":
            for _ in range(20):
                BookAuthor.objects.create(
                    full_name=fake.name(),
                    bio=fake.text()
                )
        elif kwargs["object"] == "book":
            for _ in range(200):
                Book.objects.create(
                    title=fake.sentence(nb_words=4),
                    author=random.choice(BookAuthor.objects.all()),
                    description=fake.text(),
                    published_date=fake.date_this_decade()
                )
        else:
            self.stdout.write(self.style.ERROR('Invalid object type. Please use "book" or "author".'))
            return

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data.'))