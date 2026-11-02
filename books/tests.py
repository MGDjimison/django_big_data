from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from books.models import Book, BookAuthor, Loan


class BookLoanTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="reader@example.com",
            password="test-password-123",
        )
        self.author = BookAuthor.objects.create(full_name="A. Writer", bio="Author")
        self.book = Book.objects.create(
            title="A Good Book",
            author=self.author,
            description="A book description",
            published_date=timezone.localdate(),
        )
        self.loan_url = reverse("book-loan", args=[self.book.pk])

    def test_loan_link_is_only_shown_to_authenticated_users(self):
        anonymous_response = self.client.get(reverse("book-list"))
        self.assertNotContains(anonymous_response, "Loan this book")

        self.client.force_login(self.user)
        authenticated_response = self.client.get(reverse("book-list"))

        self.assertContains(authenticated_response, "Loan this book")
        self.assertContains(authenticated_response, self.loan_url)

    def test_loan_confirmation_requires_authentication(self):
        response = self.client.get(self.loan_url)

        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={self.loan_url}",
        )

    def test_get_displays_confirmation_without_creating_loan(self):
        self.client.force_login(self.user)

        response = self.client.get(self.loan_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/loan_confirm.html")
        self.assertContains(response, self.book.title)
        self.assertFalse(Loan.objects.exists())

    def test_confirming_loan_creates_record_and_sends_email(self):
        self.client.force_login(self.user)

        response = self.client.post(self.loan_url)

        loan = Loan.objects.get(book=self.book, borrower=self.user)
        self.assertRedirects(
            response,
            reverse("loan-confirmed", args=[loan.pk]),
        )
        self.assertEqual(loan.return_date, timezone.localdate() + timedelta(days=14))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        self.assertIn(self.book.title, mail.outbox[0].subject)
        self.assertIn(loan.return_date.strftime("%B %d, %Y"), mail.outbox[0].body)

    def test_loan_confirmation_page_is_only_visible_to_borrower(self):
        other_user = get_user_model().objects.create_user(email="other@example.com")
        loan = Loan.objects.create(book=self.book, borrower=other_user)
        self.client.force_login(self.user)

        response = self.client.get(reverse("loan-confirmed", args=[loan.pk]))

        self.assertEqual(response.status_code, 404)

    @patch("books.views.send_mail", return_value=0)
    def test_failed_email_send_does_not_create_loan(self, send_mail_mock):
        self.client.force_login(self.user)

        with self.assertRaises(RuntimeError):
            self.client.post(self.loan_url)

        self.assertFalse(Loan.objects.exists())
