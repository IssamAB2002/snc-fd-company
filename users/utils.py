from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import send_mail
from .models import Order
from django.utils import timezone
from datetime import timedelta, datetime
import datetime
import random
from django.utils.encoding import force_bytes, force_str


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # create a hashed token using combine user's primary key and timestamp
        return (
            str(user.pk) + str(timestamp) +
            # add email verification status
            str(user.email_verified) +
            # add phone verification status
            str(user.phone_verified)
        )

account_activation_token = TokenGenerator()


def inform_managers(subject, message):
    # send email to managers to inform them about new order
    fd_email = settings.DEFAULT_FROM_EMAIL
    managers = User.objects.filter(is_manager=True)
    managers_emails = [user.email for user in managers]
    for email in managers_emails:
        if email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

# define can place order function for check user's order time


def can_place_order(user, wait_hours=2):
    # get user's last order
    last_order = Order.objects.filter(
        user=user).order_by('-created_at').first()
    # check if there's last order (or any order)
    if last_order:
        # calculate time since last order
        time_since_last_order = timezone.now() - last_order.created_at
        # calculate timedelta of now time & time since last order
        remaining_time = timedelta(hours=wait_hours) - time_since_last_order
        # check if remaining time seconds is > 0 (to be rounded)
        if remaining_time.total_seconds() > 0:
            # round remaining time to the nearest minute
            remaining_minutes = round(remaining_time.total_seconds() / 60)
            # set the new minutes to remaining time (timedelta)
            rounded_remaining_time = timedelta(minutes=remaining_minutes)
            # if remaining time is not finished return not allowed to order & remaining time
            return False, rounded_remaining_time
    # if there's no last order (or any order) return allowed & none (remaining time)
    return True, None


def is_within_allowed_time(start_hour=6, end_hour=17):
    current_time = datetime.datetime.now()
    return start_hour <= current_time.hour < end_hour

def generate_phone_verification_token():
    # generate verification token
    phone_verification_token = str(random.randint(100000, 999999))
    return phone_verification_token