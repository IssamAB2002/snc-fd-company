from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    # home url
    path('', views.home, name='home'),
    # blogs url
    # path('blog/', views.blog, name='blog'),
    # blog details url
    # path('blog_details/', views.blog_details, name='blog_details'),
    # contact url
    path('contact/', views.contact, name='contact'),
]