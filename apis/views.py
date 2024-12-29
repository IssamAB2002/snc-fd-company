from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# import token obtainer view
from rest_framework_simplejwt.views import TokenObtainPairView
# import permession 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
# import rest framework built-in views
from rest_framework.views import APIView
from rest_framework import status, generics
import random
# import custom serializers 
from .serializers import * 
from .models import AndroidApp
from users.utils import generate_phone_verification_token
from users.models import User
from users.utils import is_within_allowed_time, can_place_order
from core.models import BannerArticle 
from shopping.models import Article


# def the custom token provider view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
# def the user data provider view 
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

# def registration view
class UserRegistrationView(APIView):
    # def post func to fetch request data 
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # send verification emails/
            if user.email:
                message = ''
                # check if the stored code is not expired
                if user.is_code_valid(personal_code=user.email_verification_code, code=user.email_verification_code, expiry=user.email_code_expires_at):
                    message = f'Your Verification Code is: {user.email_verification_code}'
                else:
                    user.set_verification_codes()
                    message = f'Your Verification Code is: {user.email_verification_code}'
                user.email_user(subject='SNC FD Email Verification', message=message)                
            return Response(
                {"message": "User registered successfully. Verify your email to activate the account."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
# def verification view
class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email)
            if user.is_code_valid(personal_code=user.email_verification_code, code=code, expiry=user.email_code_expires_at):
                user.email_verified = True
                user.is_active = True
                user.save()
                return Response({"message": "Email successfully verified."}, status=status.HTTP_200_OK)
            else: 
                return Response({"error": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
# define re-send an email verification:
class ReSendVerificationEmail(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        user.set_verification_codes()
        user.email_user(subject='SNC FD Email Verification', 
                        message=f'Your Verification Code is: {user.email_verification_code}')
        return Response({"message": "Verification code resent successfully."}, status=status.HTTP_200_OK)
class SendPasswordCode(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        if user is None:
            return Response({'mesage': 'Invalid Email'}, status=status.HTTP_404_NOT_FOUND)   
        user.set_password_reset_code()
        user.save()
        print(f"User's Code: {user.password_reset_code}")
        print(f"User's Expiry: {user.password_code_expires_at}")
        try:
            user.email_user(subject='SNC FD Password Reset',
                            message=f'Your Password Reset Code is: {user.password_reset_code}')
        except:
            return Response({"error": "Failed to send password reset code."}, status=status.HTTP_400)
        return Response({'message': 'Password Reset Code is sent'}, status=status.HTTP_200_OK)
class checkPasswordCode(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        print(f'Sent Code: {code}')
        user = User.objects.get(email=email)
        print(f'User Stored Code: {user.password_reset_code}')
        print(f'User Code Expiry: {user.password_code_expires_at}')
        if user is None:
            return Response({'mesage': 'Invalid Email'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_code_valid(personal_code=user.password_reset_code, code=code, expiry=user.password_code_expires_at):
            return Response({"message": "Password reset code is valid."}, status=status.HTTP_200_OK)
        else: 
            return Response({"error": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)
class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)
        if user is None:
            return Response({'mesage': 'Invalid Email'}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(password)
        user.save()
        return Response({'message': 'Password is reset successfully'}, status=status.HTTP_200_OK)
# define the blogs api view
class BlogListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = BannerArticle.objects.filter(is_active=True)
    serializer_class =  BannerArticleSerializer
    
# def the article api view
class ArticleListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        # Get the query parameters
        new_products = request.query_params.get('new', None)
        random_products = request.query_params.get('random', None)

        if new_products:  # If 'new' is in the query, get the most recent products
            products = Article.objects.order_by('-created_at')[:int(new_products)]
        elif random_products:  # If 'random' is in the query, get random products
            products = Article.objects.order_by('?')[:int(random_products)]
        else:  # Otherwise, return all products
            products = Article.objects.all()

        # Serialize and return the response
        serializer = ArticleSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class =  CategorySerializer
    
class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('id', None)
        if order_id:
            order = get_object_or_404(Order, id=order_id, user=request.user)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.filter(user=request.user).prefetch_related('items__article')
            serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not request.user.phone_verified:
            return Response({'error': 'you have to wait until we verifiy you identity, thank you for understanding.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not is_within_allowed_time():
            return Response({'error': 'Orders can only be placed between 6 AM and 5 PM.'}, status=status.HTTP_400_BAD_REQUEST)
        # get allowed and wait time from can place order
        allowed, wait_time = can_place_order(request.user, wait_hours=2)
        if not allowed:
        # if not allowed get wait hours & minutes from wait time
            wait_hours = wait_time.total_seconds() // 3600
            wait_minutes = (wait_time.total_seconds() % 3600) // 60
        # inform user must wait (wait time)
            return Response({'error': f'You must wait {int(wait_hours)} h and {int(wait_minutes)} m before placing order again'}) 
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {
                    "message": "Order created successfully.",
                    "order": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
def get_latest_apk(request):
    latest_app = AndroidApp.objects.order_by('-uploaded_at').first()
    if latest_app:
        return JsonResponse({
            "version": latest_app.version,
            # "apk_url": request.build_absolute_uri(latest_app.apk_file.url),
        })
    return JsonResponse({"error": "No APK available"}, status=404)

def app_download_page(request):
    latest_version = AndroidApp.objects.order_by('-id').first()  # Fetch the latest version
    return render(request, 'core/android_app.html', {'app_version': latest_version})


    
