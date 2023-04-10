from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.conf import settings

from .forms import SignupForm, LoginForm

# Create your views here.


class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"


class UserLogoutView(LogoutView):
    pass

