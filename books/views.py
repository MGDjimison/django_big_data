from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from books.models import Book, Loan

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache the view for 15 minutes
class BookListView(ListView):
    model = Book
    queryset = Book.objects.select_related('author').only('title', 'author__full_name', 'published_date')
    template_name = 'books_list.html'
    context_object_name = 'books'
    ordering = ['-published_date', "-pk"]
    paginate_by = 20


@login_required
def loan_book(request, pk):
    book = get_object_or_404(Book.objects.select_related("author"), pk=pk)

    if request.method == "POST":
        with transaction.atomic():
            loan = Loan.objects.create(book=book, borrower=request.user)
            sent_count = send_mail(
                subject=f"Your loan is confirmed: {book.title}",
                message=(
                    f"Your loan of '{book.title}' is confirmed.\n"
                    f"Please return it by {loan.return_date:%B %d, %Y}."
                ),
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            if sent_count != 1:
                raise RuntimeError("The loan confirmation email was not sent.")
        return redirect("loan-confirmed", loan_id=loan.pk)

    return render(request, "books/loan_confirm.html", {"book": book})


@login_required
def loan_confirmed(request, loan_id):
    loan = get_object_or_404(
        Loan.objects.select_related("book", "book__author"),
        pk=loan_id,
        borrower=request.user,
    )
    return render(request, "books/loan_confirmed.html", {"loan": loan})

 