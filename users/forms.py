from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from users.models import User


@deconstructible
class RussianValidator:
    """
    Валидатор для заполнения имени и фамилии
    """
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    code = 'russian'

    def __init__(self):
        self.message = "Должны быть только русские буквы"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class UserLoginForm(AuthenticationForm):
    """
    Форма для входа на спйт
    """
    password = forms.CharField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )


class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации на сайте
    """
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',

        )

    first_name = forms.CharField(validators=[
        RussianValidator(),
    ])
    last_name = forms.CharField(validators=[
        RussianValidator(),
    ])
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class ProfileForm(UserChangeForm):
    """
    Форма профиля
    """
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()


class UpdateUser(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )

    first_name = forms.CharField(validators=[
        RussianValidator(),
    ])
    last_name = forms.CharField(validators=[
        RussianValidator(),
    ])


class RestorePassword(AuthenticationForm):
    """
    Форма для восстановления пароля
    """
    class Meta:
        model = User
        fields = (
            'email',
        )


class ChangePasswordForm(UserChangeForm):
    """
    Форма для  изменения пароля
    """
    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
            'new_pass_rep',
        )

    old_password = forms.CharField()
    new_password = forms.CharField()
    new_pass_rep = forms.CharField()

    def clean(self):
        """
        Валидатор для проверки нового пароля
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_pass_rep')
        data_new_password = cleaned_data.get('new_password')
        old_password = cleaned_data.get('old_password')

        if old_password == data_new_password:
            raise forms.ValidationError('Старый и новый пароль не должны совпадать!')

        if len(data_new_password) < 7:
            raise forms.ValidationError('Пароль должен быть больше 8 символов!')

        if data_new_password != new_password:
            raise forms.ValidationError('Пароли не совпадают!')


        else:
            return data_new_password


class ChangeEmailForm(UserChangeForm):
    """
    Класс для замены почты.
    Методы:
    - clean_new_email - используется для проверки,
     не используется ли уже введенный адрес электронной почты другим пользователем.
    - save - сохраняет изменения в адресе электронной почты пользователя.
    """
    new_email = forms.CharField()
    class Meta:
        model = User
        fields = ()

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже используется.")
        return new_email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['new_email']
        if commit:
            user.save()
        return user
