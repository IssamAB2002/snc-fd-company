from django.contrib.auth.backends import BaseBackend
from .models import User

# Custom authentication backend to allow login using email or phone number
class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the username is an email or phone number and get the user
            user = User.objects.get(
                email=username) if '@' in username else User.objects.get(phone_number=username)
        except User.DoesNotExist:
            # Return None if user does not exist
            return None
        # Return the user if password matches
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            # Return the user object by ID
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Return None if user does not exist
            return None
