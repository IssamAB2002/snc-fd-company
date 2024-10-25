# import password reset view
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# import auth functions
from django.contrib.auth import get_user_model, authenticate, login, logout, get_backends
# import login required decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# import messages
from django.contrib import messages
# import Twilio credentials
from .local import *
# get object or return 404 error, render, redirect
from django.shortcuts import get_object_or_404, render, redirect
# import get current site (domain)
from django.contrib.sites.shortcuts import get_current_site
# import render to stering (html to string)
from django.template.loader import render_to_string
# import reverse lazy
from django.urls import reverse_lazy
# import http response
from django.http import HttpResponse, JsonResponse
# import safeurl base 64 encode, decode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# import force byte and force str
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
# import activation token generator
from .utils import account_activation_token, inform_managers, can_place_order, is_within_allowed_time
# import manager required decorator 
from .decorators import manager_required
# import send mail function
from django.core.mail import send_mail
from twilio.rest import Client
from shopping.cart import Cart
from .models import Order, OrderItem, User
# import reset password function
from .forms import UserRegistrationForm, EmailOrPhoneLoginForm, UserProfileUpdateForm
import random
import time
from datetime import timedelta

# View to handle registraion
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            inform_managers(
                'New User Joined', f'Hello Manager, \n{user.first_name} {user.last_name} Joined To SNC FD')

            if user.email and not user.email_verified:
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                token = account_activation_token.make_token(user)
                message = render_to_string('users/acc_activ_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                })
                user.email_user(mail_subject, message)
                messages.info(
                    request, 'A verification email has been sent to your email address.')
            else:
                messages.error(
                    request, 'Your email is already verified or not provided.')

            return render(request, 'users/registration_pending.html')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'title': 'Register', 'form': form})
# View to handle email activation
def activate(request, uidb64, token):
    # Try to decode uidb64 and get user object
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # Activate user and set email verified
        user.is_active = True
        if user.email:
            # set email verified to true
            user.email_verified = True
            # let the user know that he activated his email successfully
            messages.success(
                request, 'Your Email has been activated successfully !')
        user.save()
        # specify the backend use to authenticate the user
        # select the backend by index (setting.py AUTHENTICATEION_BACKENDS)
        backend = get_backends()[0]
        # link the user with backend
        user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
        # login (authenticate) user using the selected backend
        login(request, user, backend=user.backend)
        return redirect('core:home')
    else:
        # If invalid, render activation_invalid.html
        return render(request, 'users/activation_invalid.html')

# View to handle login


def login_view(request):
    # Check if request method is POST
    if request.method == 'POST':
        print('is a post request')
        # Initialize form with POST data
        form = EmailOrPhoneLoginForm(data=request.POST)
        print('checking if the for is valid')
        # Check if form is valid
        if form.is_valid():
            # Get username and password from form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            # Check if user is authenticated
            if user is not None:
                # specify the backend use to authenticate the user
                # select the backend by index (setting.py AUTHENTICATEION_BACKENDS)
                backend = get_backends()[0]
                # link the user with backend
                user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
                # login (authenticate) user using the selected backend
                login(request, user, backend=user.backend)
                # Redirect to home page
                return redirect('core:home')
            else:
                # Invalid username or password
                messages.error(request, 'Invalid username or password.')
                return redirect('users:login')
        else: 
            messages.error(request,'check your form validation !')
    else:
        # Initialize empty form
        form = EmailOrPhoneLoginForm()
    # Render login template
    return render(request, 'users/login.html', {'title': 'Log in', 'form': form})

# View to handle verifying email


@login_required
def verify_email(request):
    # get user
    user = request.user
    # check if the user has email & not verified
    if user.email and not user.email_verified:
        # get domain name
        current_site = get_current_site(request)
        # mail message subject
        mail_subject = 'Activate your account.'
        # mail message body
        message = render_to_string('users/acc_activ_email.html', {
            # user model
            'user': user,
            # domain
            'domain': current_site.domain,
            # encode uid for user
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            # user verification token
            'token': account_activation_token.make_token(user),
        })
        # send the verification token
        user.email_user(mail_subject, message)
        # let user know that verification email is sent
        messages.info(
            request, 'A verification email has been sent to your email address.')
    else:
        # if user is not none set error message user not exist
        messages.error(
            request, 'Your email is already verified or not provided.')
    return render(request, 'users/registration_pending.html')

# View to handle logout


def logout_view(request):
    user = request.user
    logout(request)
    return redirect('core:home')

# View to handle phone number activation

@login_required(redirect_field_name='users:login')
def verify_phonenumber(request):
    user = request.user
    phone_number = user.phone_number
    if phone_number:
        if phone_number.startswith('0'):
            phone_number = '+213' + phone_number[1:]
        else: 
            messages.error(request, 'Phone Number must starts with 0 !')
            return redirect('users:dashboard')
    # check if the user is authenticated
    if user.is_authenticated:
        # check if user's phone is verified
        if user.phone_verified:
            # if verified redirect to home page
            messages.warning(request, 'Your Phone Number is already Verified !')
            return redirect('core:home')
        # Handle requesting a verification code
        # define the client variable (admin)
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # generate verification token
        phone_verification_token = str(random.randint(100000, 999999))
        # stor verification token in session
        request.session['verification_token'] = phone_verification_token
        # set expiry time (5 minutes) for security
        request.session['verification_expiry'] = time.time() + 300
        try:
            # create verification including user's phone number
            verification = client.messages.create(
                body=f"Your Verification Code is {phone_verification_token}",
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            # redirect to verfication form
            return render(request, 'users/verification_form.html', {'status': 'Verification code sent'})
        # make error if it didn't work
        except Exception as e:
            return render(request, 'users/verification_form.html', {'error': e})

    # Redirect to login if user is not authenticated
    return redirect('users:login')

# View to handle verifiaction of SMS code


def verify_code(request):
    # check if the method is POST
    if request.method == 'POST':
        user = request.user
        # get the code from the form
        verification_code = request.POST.get('verification_code')
        if not verification_code:
            return render(request, 'users/verification.html', {'error': 'verification code must be set'})
        # get verification token from session
        stored_token = request.session.get(
            'verification_token')
        # get expiry time from session
        code_expiry = request.session.get('verification_expiry')
        # check if token has expired
        if time.time() > code_expiry:
            # if so raise error
            return JsonResponse({'error': 'Token has expired'}, status=400)
        # check validation of token
        if verification_code == stored_token:
            # set phone to verified
            user.phone_verified = True
            user.save()
            # return success message
            messages.success(
                request, 'Your phone number was verified successfully')
            # delete verification token from session
            del request.session['verification_token']
            # redirect home
            return redirect('core:home')
        else:
            # if not return error message
            return render(request, 'users/verification_form.html', {'error': 'invalid verification code'})

    return render(request, 'users/verification_form.html')


@login_required(redirect_field_name='users:login')
def create_order(request):
    # import request session cart
    cart = Cart(request)
    # Check if user is allowed to order
    # check if user phone number is verified
    if not request.user.phone_verified:
        messages.error(request, 'Please Verify your Phone Number, So you place order !')
        return redirect('users:dashboard')
    # check if time within the allowed time range
    if not is_within_allowed_time():
        messages.error(
            request, 'Orders can only be placed between 6 AM and 5 PM.')
        return redirect('shopping:card_details')
    # get allowed and wait time from can place order
    allowed, wait_time = can_place_order(request.user, wait_hours=2)
    if not allowed:
        # if not allowed get wait hours & minutes from wait time
        wait_hours = wait_time.total_seconds() // 3600
        wait_minutes = (wait_time.total_seconds() % 3600) // 60
        # inform user must wait (wait time)
        messages.error(
            request, f'You must wait {int(wait_hours)} h and {int(wait_minutes)} m before placing order again')
        return redirect('shopping:card_details')
    # if is allowed check if cart has article
    if len(cart) == 0:
        # if not seend message to user
        messages.warning(
            request, "you don't have any articles in your cart yet")
        return redirect('shopping:card_details')
    # if cart has articles create order
    order = Order.objects.create(
        # user
        user=request.user,
        # total price
        total_price=cart.get_total_price(),
        # is sent to delivery
        is_sent=False,
        # set last updated to now
        last_updated=timezone.now(),
        # update time to 0
        update_times=0,
        # pick up date
        pickup_date=timezone.now() + timedelta(days=1)
    )
    # create order items
    for item in cart:
        # get article & quantity from cart
        article = item['article']
        quantity = item['quantity']
        # check if article is available, if not inform user
        if not article.available:
            messages.warning(
                request, f'{article.name} is currently sold out !')
            redirect('core:home')
        # check if article is in order item for the current order (to prevent repeat)
        order_item_article = OrderItem.objects.filter(
            article=article, order=order)
        if order_item_article.exists():
            order_item_article.quantity += quantity
        # if not create item with specified infos
        else:
            OrderItem.objects.create(
                order=order,
                article=article,
                quantity=quantity,
                price=item['price']
            )
    # set order last updated to now
    order.last_updated = timezone.now()
    # save order
    order.save()
    # clear cart
    cart.clear()
    inform_managers(f'{order.user.first_name.capitalize()} {order.user.last_name.capitalize()} Placed New Order',
                    f'Order ID: {order.id}\nTotal: {order.total_price}\nPlaced by: {order.user.first_name} { order.user.last_name }')
    messages.success(
        request, 'Your Order has been sent to the Company')
    return render(request, 'users/confirmation.html', {'title': 'Order Confirmation' ,'order': order})

# define order list view
@manager_required
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        print(order.is_printed)
    return render(request, 'users/admin_orders_view.html', {'title': 'Orders View', 'orders': orders})

# define order details view


@manager_required
def admin_order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'users/order_details.html', {'title': 'Order Details', 'order': order})

# define order print view


@manager_required
def admin_order_print(request, order_id):
    order = Order.objects.get(id=order_id)
    if not order.is_printed: 
        order.is_printed = True
        order.save() 
    return render(request, 'users/order_print.html', {'order': order})

login_required(redirect_field_name='users:login')
def client_order_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'title': 'Client Orders List',
        'orders': orders,
    }
    return render(request, 'users/client_order_list.html', context)


login_required(redirect_field_name='users:login')
def client_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'title': 'Client Order Details',
        'order': order,
    }
    return render(request, 'users/client_order_details.html', context)

@login_required(redirect_field_name='users:login')
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    if len(orders) <= 0:
        print('NO ORDERS')
    else:
        for order in orders:
            print(order.user.email)
    return render(request, 'users/dashboard.html', context)


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:dashboard')
    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, 'users/update_profile.html', {'form': form})
