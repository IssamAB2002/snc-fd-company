from django.urls import path
from .views import *
app_name = 'users'
urlpatterns = [
    # add login, register & logout urls
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('verify_email/', verify_email, name='verify_email'),
    path('verify_phonenumber/', verify_phonenumber, name='verify_phonenumber'),
    path('verify_code/', verify_code, name='verify_code'),
    path('confirm', create_order, name='confirm'),
    # define admin orders list url
    path('admin/orders_view', admin_order_list, name='admin_orders_view'),
    # define admin order details url
    path('admin/orders/<int:order_id>/',
         admin_order_detail, name='admin_order_detail'),
    # define admin order print url
    path('admin/orders/<int:order_id>/print/',
         admin_order_print, name='admin_order_print'),
    path('client_order_list', client_order_list, name='client_order_list'),
    path('client_order_details/<int:order_id>/', client_order_details, name='client_order_details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('update-profile/', update_profile, name='update_profile'),
]

