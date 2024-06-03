from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator

from orders.models import OrderItem


def send_email_order(request, user, order, template_name, title_email):
    user = request.user
    current_site = get_current_site(request)
    products = OrderItem.objects.filter(order=order)
    context = {
        'user': user,
        'order': order,
        'domain': current_site.domain,
        'OrderItem': products,
    }
    message = render_to_string(template_name=template_name,
                               context=context)
    email = EmailMessage(
        title_email,
        message,
        to=[user.email], )
    email.send()
