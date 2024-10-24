from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from .models import BannerArticle
from shopping.models import Article, Category
from shopping.utils import random_slice
from .models import ContactMessage
# home view


def home(request):
    categories = Category.objects.prefetch_related('subcategory_set').all()
    latest_articles = Article.objects.all().order_by('-created_at')[0:8]
    random_articles = random_slice(Article.objects.all(), 8)
    sold_articles = Article.objects.filter(deal_end_time__gte=timezone.now())
    print(sold_articles)
    banner_art = BannerArticle.objects.all()
    context = {
        'title': 'Home',
        'banner_articles': banner_art,
        'sold_articles': sold_articles,
        'latest_articles': latest_articles,
        'random_articles': random_articles,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)
# blog view


def blog(request):
    context = {
        'title': 'Blog',
    }
    return render(request, 'core/blog.html', context)
# blog detai;s view


def blog_details(request):
    context = {
        'title': 'Blog Details',
    }
    return render(request, 'core/blog_details.html', context)
# contact view


def contact(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            contact_message = ContactMessage(subject=subject, message=message, user=request.user)
            contact_message.save()
            messages.success(request, 'We recieved your message')
        else:
            messages.error(request, 'You must to log in, so you can send us message !')
            redirect('core:contact')
    context = {
        'title': 'Contact',
    }
    return render(request, 'core/contact.html', context)
