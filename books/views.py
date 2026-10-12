from django.views.generic.list import ListView

from books.models import Book


class BookListView(ListView):
    model = Book
    queryset = Book.objects.select_related('author')
    template_name = 'books_list.html'
    context_object_name = 'books'
    ordering = ['-published_date']
    paginate_by = 20

    
    
    