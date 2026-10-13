from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from books.models import Book

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache the view for 15 minutes
class BookListView(ListView):
    model = Book
    queryset = Book.objects.select_related('author').all()
    template_name = 'books_list.html'
    context_object_name = 'books'
    ordering = ['-published_date']
    paginate_by = 20

 