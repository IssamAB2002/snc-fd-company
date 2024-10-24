
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
# import user model
from .models import User, ALGERIAN_WILAYAS

# registeration form


class UserRegistrationForm(UserCreationForm):
    # first name & last name field
    first_name = forms.CharField(
        label='First Name',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(
        label='Last Name',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    # add email field with form control class
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    # phone number field with form control class
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'ex. 0555847328'})
    )
    state = forms.ChoiceField(
        label='Wilaya',
        choices=ALGERIAN_WILAYAS,
        widget=forms.Select(attrs={'class': 'form-control py-2 w-100'})
    )

    # City field as a CharField
    city = forms.CharField(
        label='City',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )

    # Street field as a CharField
    street = forms.CharField(
        label='Street',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    # second phone number field
    sec_phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Second Phone Number'})
    )

    # add password field with form control class
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    # Add password confirmation field with form control class
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    # Define form metadata
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'state', 'city', 'street', 'sec_phone_number',
                  'email', 'phone_number', 'password1', 'password2')

    # Override clean method for custom validation
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')
        street = cleaned_data.get('street')
        email = cleaned_data.get('email')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Check if the phone number starts with 0 and has exactly 10 digits
            if not phone_number.startswith('0'):
                raise ValidationError('Phone number must start with 0.')
            if len(phone_number) != 10:
                raise ValidationError(
                    'Phone number must be exactly 10 digits long.')
            if not phone_number.isdigit():
                raise ValidationError('Phone number must contain only digits.')
        return phone_number

    def clean_sec_phone_number(self):
        sec_phone_number = self.cleaned_data.get('sec_phone_number')

        if sec_phone_number:
            # Check if the second phone number starts with 0 and has exactly 10 digits
            if not sec_phone_number.startswith('0'):
                raise ValidationError('Second phone number must start with 0.')
            if len(sec_phone_number) != 10:
                raise ValidationError(
                    'Second phone number must be exactly 10 digits long.')
            if not sec_phone_number.isdigit():
                raise ValidationError(
                    'Second phone number must contain only digits.')
        return sec_phone_number
# login form


class EmailOrPhoneLoginForm(AuthenticationForm):
    # Define a char field for Email or Phone
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email or Phone Number'}) 
    )
    # Define a char field for Password
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})  
    )


class UserProfileUpdateForm(forms.ModelForm):
    # first name & last name field
    first_name = forms.CharField(
        label='First Name',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(
        label='Last Name',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    # add email field with form control class
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    # phone number field with form control class
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    state = forms.ChoiceField(
        label='Wilaya',
        choices=ALGERIAN_WILAYAS,
        widget=forms.Select(
            attrs={'class': 'form-control w-100'})
    )

    # City field as a CharField
    city = forms.CharField(
        label='City',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City'})
    )

    # Street field as a CharField
    street = forms.CharField(
        label='Street',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    # second phone number field
    sec_phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Second Phone Number'})
    )


    # Define form metadata
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'state', 'city', 'street', 'sec_phone_number',
                  )

    # Override clean method for custom validation
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')
        street = cleaned_data.get('street')
        email = cleaned_data.get('email')
        return cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Check if the phone number starts with 0 and has exactly 10 digits
            if not phone_number.startswith('0'):
                raise ValidationError('Phone number must start with 0.')
            if len(phone_number) != 10:
                raise ValidationError(
                    'Phone number must be exactly 10 digits long.')
            if not phone_number.isdigit():
                raise ValidationError('Phone number must contain only digits.')
        return phone_number

    def clean_sec_phone_number(self):
        sec_phone_number = self.cleaned_data.get('sec_phone_number')

        if sec_phone_number:
            # Check if the second phone number starts with 0 and has exactly 10 digits
            if not sec_phone_number.startswith('0'):
                raise ValidationError('Second phone number must start with 0.')
            if len(sec_phone_number) != 10:
                raise ValidationError(
                    'Second phone number must be exactly 10 digits long.')
            if not sec_phone_number.isdigit():
                raise ValidationError(
                    'Second phone number must contain only digits.')
        return sec_phone_number
