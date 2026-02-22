from django.contrib.auth.views import LoginView
from users.forms import UserLoginForm


class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = UserLoginForm
