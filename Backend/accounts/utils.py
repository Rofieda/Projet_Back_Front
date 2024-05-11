from django.core.mail import EmailMessage
from django.conf import settings
from .models import User
from django.contrib.sites.shortcuts import get_current_site


def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email='llmcsquest@gmail.com',
        to=[data['to_email']]
    )
    email.send()
