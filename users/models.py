from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from shopping.models import Article

ALGERIAN_WILAYAS = [
    ('Adrar', 'Adrar'),
    ('Chlef', 'Chlef'),
    ('Laghouat', 'Laghouat'),
    ('Oum El Bouaghi', 'Oum El Bouaghi'),
    ('Batna', 'Batna'),
    ('Bejaia', 'Bejaia'),
    ('Biskra', 'Biskra'),
    ('Bechar', 'Bechar'),
    ('Blida', 'Blida'),
    ('Bouira', 'Bouira'),
    ('Tamanrasset', 'Tamanrasset'),
    ('Tebessa', 'Tebessa'),
    ('Tlemcen', 'Tlemcen'),
    ('Tiaret', 'Tiaret'),
    ('Tizi Ouzou', 'Tizi Ouzou'),
    ('Algiers', 'Algiers'),
    ('Djelfa', 'Djelfa'),
    ('Jijel', 'Jijel'),
    ('Setif', 'Setif'),
    ('Saïda', 'Saïda'),
    ('Skikda', 'Skikda'),
    ('Sidi Bel Abbes', 'Sidi Bel Abbes'),
    ('Annaba', 'Annaba'),
    ('Guelma', 'Guelma'),
    ('Constantine', 'Constantine'),
    ('Medea', 'Medea'),
    ('Mostaganem', 'Mostaganem'),
    ('Msila', 'Msila'),
    ('Mascara', 'Mascara'),
    ('Ouargla', 'Ouargla'),
    ('Oran', 'Oran'),
    ('El Bayadh', 'El Bayadh'),
    ('Illizi', 'Illizi'),
    ('Bordj Bou Arreridj', 'Bordj Bou Arreridj'),
    ('Boumerdes', 'Boumerdes'),
    ('El Tarf', 'El Tarf'),
    ('Tindouf', 'Tindouf'),
    ('Tissemsilt', 'Tissemsilt'),
    ('El Oued', 'El Oued'),
    ('Khenchela', 'Khenchela'),
    ('Souk Ahras', 'Souk Ahras'),
    ('Tipaza', 'Tipaza'),
    ('Mila',
     'Mila'),
    ('Aïn Defla', 'Aïn Defla'),
    ('Naama', 'Naama'),
    ('Aïn Temouchent', 'Aïn Temouchent'),
    ('Ghardaia', 'Ghardaia'),
    ('Relizane', 'Relizane'),
    ('Timimoun', 'Timimoun'),
    ('Bordj Badji Mokhtar', 'Bordj Badji Mokhtar'),
    ('Ouled Djellal', 'Ouled Djellal'),
    ('Béni Abbès', 'Béni Abbès'),
    ('In Salah', 'In Salah'),
    ('In Guezzam', 'In Guezzam'),
    ('Touggourt', 'Touggourt'),
    ('Djanet', 'Djanet'),
    ('El M’Ghaier', 'El M’Ghaier'),
    ('El Meniaa', 'El Meniaa')
]
# Custom manager for the User model


class UserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError(
                'Users must have an email address or phone number')
        user = self.model(email=email, phone_number=phone_number)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)  # Save the user object in the database
        return user

    # Method to create a superuser
    def create_superuser(self, email, phone_number, password, **extra_fields):
        user = self.create_user(
            email=email, phone_number=phone_number, password=password, **extra_fields)
        # Set the user as an admin
        user.is_admin = True
        # Set the user as a staff
        user.is_staff = True
        user.is_manager = True
        # Set the user as a super user
        user.is_superuser = True
        user.save(using=self._db)
        return user
# Custom user model


class User(AbstractBaseUser, PermissionsMixin):
    # First name & lasr name
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    # Email field, can be null
    email = models.EmailField(unique=True, null=True, blank=True)
    # Phone number field, can be null
    phone_number = models.CharField(
        max_length=15, unique=True, null=True, blank=True)
    # state field
    state = models.CharField(max_length=50, null=True, choices=ALGERIAN_WILAYAS)
    city = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=100, null=True)
    # second phone number
    sec_phone_number = models.CharField(max_length=15, null=True, blank=True)
    # field to check if the user is active
    is_active = models.BooleanField(default=True)
    # field to check if the user is an admin
    is_admin = models.BooleanField(default=False)
    # field to check if the user is staff
    is_staff = models.BooleanField(default=False)
    # field to check if the user is a manager
    is_manager = models.BooleanField(default=False)
    # fields to check if the user's email & phone is verified
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    # Specify the custom manager
    objects = UserManager()
    # Use email as the username field
    USERNAME_FIELD = 'email'
    # Phone number is also required
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        # Return email or phone number as string representation
        return f'{self.last_name} {self.first_name}'

    def has_perm(self, perm, obj=None):
        # Admins have all permissions
        return self.is_admin

    # Function to send verification code to user by email & phone
    def email_user(self, subject, message, **kwargs):
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [self.email], **kwargs)

    def send_sms(self, message):
        pass

    def has_module_perms(self, app_label):
        # Admins have permissions for all modules
        return self.is_admin

    def save(self, *args, **kwargs):
        # Get the original values from the database
        original_user = User.objects.get(pk=self.pk) if self.pk else None

        # Check if email or phone number has changed
        if original_user:
            if original_user.email != self.email:
                self.email_verified = False
            if original_user.phone_number != self.phone_number:
                self.phone_verified = False

        super(User, self).save(*args, **kwargs)
    def full_address(self):
        return f'{self.state}, {self.city}, {self.street}'
# create order model


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    update_times = models.PositiveIntegerField()
    is_sent = models.BooleanField(default=False)
    pickup_date = models.DateField(null=False, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_printed = models.BooleanField(default=False)
    def __str__(self):
        return f"Order {self.id} by {self.user.first_name} {self.user.last_name}"

# create order item model


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.article.name}"

    def get_total_price(self):
        return self.price * self.quantity
