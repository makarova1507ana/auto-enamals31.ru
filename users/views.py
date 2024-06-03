from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.forms import forms
from django.shortcuts import render

from django.contrib import auth, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator

from users.forms import UserLoginForm, UserRegistrationForm, UpdateUser, ChangePasswordForm, ChangeEmailForm

from carts.models import Cart
from users.models import User
from users.utils import send_email_for_varify
from allauth.account.views import SignupView, LoginView, PasswordResetView


class EmailVerify(View):
    """
    Класс для верификации почты
    """
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('main:index')
        return redirect('user:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            users = User.objects.all()

            for user in users:
                if user.id == int(uid):
                    return user
        except (
                TypeError,
                ValueError,
                OverflowError,
                ValidationError,
        ):
            user = None
            return user


def login(request, user=None):
    if user:
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse('main:index'))
    if request.user.is_authenticated:
        return render(request, 'main/index.html')
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if not user.email_verify:
                send_email_for_varify(request, user)
                return HttpResponseRedirect(reverse('user:confirm_email'))
            if user:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'{username} Вы вошли в аккаунт!')

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save(form)

            session_key = request.session.session_key

            user = form.instance

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            send_email_for_varify(request=request, user=user)
            return redirect('user:confirm_email')
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)


@login_required()
def profile(request):
    """
    Функция отображения профиля
    """
    form = UserRegistrationForm(instance=request.user)
    context = {
        'title': 'Кабинет',
        'form': form,
    }
    return render(request, 'users/profile.html', context)


@login_required()
def logout(request):
    """
    Функция выхода
    """
    messages.success(request, 'Вы вышли из аккаунта!')
    auth.logout(request)
    context = {
        'title': 'Выход',
    }
    return redirect(reverse('main:index'))


def rename(request):
    """
    Функция изменения фамилии и имени
    """
    if request.method == "POST":
        form = UpdateUser(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save(form)
            messages.success(request, 'Профиль обновлен!')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserRegistrationForm(instance=request.user)
    context = {
        'title': 'Кабинет',
        'form': form,
    }
    return render(request, 'users/rename_user.html', context)


def change_profile(request):
    """
    Изменения профиля
    """
    return render(request, 'users/change_data_profile/main_change.html')

