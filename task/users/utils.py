from django.contrib.auth.tokens import default_token_generator as token_generatop
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from task import settings


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':token_generatop.make_token(user)
    }
    message = render_to_string('users/confirm_email.html', context)
    email = EmailMessage(
        'Verify email',
        message,
        from_email=settings.EMAIL_HOST_USER, 
        to=[user.email],
    )
    email.send()
    