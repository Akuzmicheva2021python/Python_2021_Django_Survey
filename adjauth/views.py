from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm, SomeAuthenticationForm
from .admin import User
from django.shortcuts import render


class MyLoginView(LoginView):
    form_class = SomeAuthenticationForm
    template_name = 'registration/login.html'


class MyLogoutView(LogoutView):
    pass


class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy('main_page')
    form_class = RegisterUserForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/../survay/templates/survay/register.html'
    success_url = reverse_lazy('login')