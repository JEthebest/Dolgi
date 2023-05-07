from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

from apps.users.forms import UserForm


class UserRegistrationView(FormView):
    template_name = 'users/register.html'
    form_class = UserForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        print(user)
        make_password(user.password)
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = 'home'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(FormView):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = PasswordResetForm
    success_url = '/password_reset/done/'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = '/password_reset/complete/'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


@login_required
def home(request):
    return render(request, 'users/base.html')

@login_required
def unauthorized_menu(request):
    return render(request, 'users/unauthorized_menu.html')