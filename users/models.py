from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(blank=True)
    email = models.EmailField(unique=True, blank=True)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email},{self.id}'
