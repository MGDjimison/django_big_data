from allauth.account.views import LoginView
from allauth.account.views import SignupView
from django.urls import reverse_lazy


class CustomSignupView(SignupView):
    template_name = "account/signup.html"
    success_url = reverse_lazy("book-list")


class CustomLoginView(LoginView):
    template_name = "account/login.html"
    success_url = reverse_lazy("book-list")


