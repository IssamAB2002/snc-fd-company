from django.urls import path
from . import views
app_name = 'shopping'
urlpatterns = [
    path('', views.shop, name='shop'),
    path('article_details/<str:slug>', views.article_details, name='article_details'),
    # card details url
    path('card_details', views.card_details, name='card_details'),
    # add product to card url
    path('card/add/', views.add_card, name='add_card'),
    # remove product from card url
    path('card/remove/<int:id>', views.card_remove, name='card_remove'),
    # clear all the card
    path('card/clear', views.clear_card, name='clear_card'),
]