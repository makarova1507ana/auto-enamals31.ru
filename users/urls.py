from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy, include
from django.views.generic import TemplateView

from .views import login, registration, profile, logout, rename, EmailVerify, change_profile

app_name = 'user'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),

    # Отображение страницы с сообщением о том что оно отправлено
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>', EmailVerify.as_view(), name='verify_email'),
    path(
        'invalid_verify', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'
    ),

    path('restore-password/', PasswordResetView.as_view(
        template_name='users/restore_password.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy("user:restore_password_done")
    ),
         name='restore_password'),
    path('restore-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='restore_password_done'),
    path('restore-password/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy("user:restore_password_complete"),
    ),
         name='password_reset_confirm'),

    path('restore-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='restore_password_complete'),

    path('profile/', profile, name='profile'),
    path('rename/', rename, name='rename'),
    path('change-profile/', change_profile, name='change_profile'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='users/change_data_profile/change_password.html',
        success_url=reverse_lazy("user:change_done")
    ),
         name='change_password'),
]
