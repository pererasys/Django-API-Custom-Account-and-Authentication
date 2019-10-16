
# Written by Andrew Perera
# Copyright 2019

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client
from .models import *
import random


@receiver(post_save, sender=get_user_model())
def generate_verification_code(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        verification_code = random.randint(9999, 99999)
        code = VerificationCode.objects.create(
            account=instance, code=verification_code)
        code.save()
        account_sid = settings.TWILIO_ACCOUNT_ID
        auth_token = settings.TWILIO_API_KEY
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body="Your verification code: " + str(code.code),
                from_=settings.TWILIO_VERIFICATION_NUMBER,
                to=str(instance.phone_number)
            )
    return
