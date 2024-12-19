from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
app_name = 'api'
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('verify-email/resend/', ReSendVerificationEmail.as_view(), name='resend_verification_email'),
    path("password-code-send/", SendPasswordCode.as_view(), name="password-code-send"),
    path("password-code-check/", checkPasswordCode.as_view(), name="password-code-check"),
    path("password-reset/", ResetPasswordView.as_view(), name="password-reset"),
    path('blog/', BlogListView.as_view(), name='blogs'),
    path('article/', ArticleListView.as_view(), name='artilce'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('orders/', OrderAPIView.as_view(), name='order-list'),  
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail')
]
