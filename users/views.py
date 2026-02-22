from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserLoginForm, UserRegisterForm


class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = UserLoginForm


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
