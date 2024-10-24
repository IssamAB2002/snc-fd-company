from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Max, Min, Q
from .models import Category, SubCategory, Article, Brand, ArticleImage, ArticleSpecification
from .forms import FilterForm
from .cart import Cart
from .utils import random_slice
def shop(request):
    # get filter form
    form = FilterForm(request.GET)
    # fetch all articles
    all_articles = Article.objects.prefetch_related('images').all()
    # fetch all categories
    categories = Category.objects.prefetch_related('subcategory_set').all()
    # Fetch 6 brands (just 6)
    all_brands = Brand.objects.all()
    # how many to display
    brand_num_to_display = 6
    # define brands
    brands = []
    # check if brands num is less than the wanted
    if len(all_brands) < brand_num_to_display:
        # if yes get all brands
        brands = all_brands
    else:
        # else slice random array from brands
        brands = random_slice(all_brands, brand_num_to_display)
    # fetch the selected category or empty string if it null
    category_id = request.GET.get('category', '')
    # fetch the selected brand or empty strung if it null
    brand_id = request.GET.get('brand', '')
    # filter articles by category
    if category_id:
        all_articles = all_articles.filter(subcategory=category_id)
    # filter articles by brand
    if brand_id.isdigit():
        brand_id = int(brand_id)
        all_articles = all_articles.filter(brand=brand_id)
    else:
        brand_id = None
    # check if the form is valid
    if form.is_valid():
        # get query if exist
        query = form.cleaned_data['query']
        if query:
            # split query into list
            query_words = query.split()
            print(query_words)
            # for each word in the query words 
            for word in query_words:
                # filter articles by word
                all_articles = all_articles.filter(
                name__icontains=word)
        # get the min price if exist
        if form.cleaned_data['min_price']:
            all_articles = all_articles.filter(
                wholesale_price__gte=form.cleaned_data['min_price'])
        # get the max price if exist
        if form.cleaned_data['max_price']:
            all_articles = all_articles.filter(
                wholesale_price__lte=form.cleaned_data['max_price'])
    # sort article by sort query
    sort = request.GET.get('sort')
    # check if the sort exist
    if sort:
        if sort == 'atoz':
            # if sort is a to z order by alphabets
            all_articles = all_articles.order_by('name')
        elif sort == 'price':
            # if sort is price order by price
            all_articles = all_articles.order_by('wholesale_price')
        elif sort == 'ztoa':
            # if sort is z to a order by alphabets in reverse
            all_articles = all_articles.order_by('-name')
    else:
        all_articles = all_articles.order_by('name')
    # define article per page, get it from request queries
    articles_per_page = request.GET.get('prp')
    if articles_per_page:
        # set products per page as prp if exist
        articles_per_page = int(articles_per_page)
    else:
        # otherwise set it to default (6)
        articles_per_page = 6
    # defne paginator with article obj & articles per page
    paginator = Paginator(all_articles, articles_per_page)  # articles per page
    # get the page num sent from front end
    page_num = request.GET.get('page')
    if page_num:
        if (int(page_num) > paginator.num_pages):
            page_num = 1
    # try to get selected objects ( articles ) via page num
    try:
        page_obj = paginator.get_page(page_num)
    # if page num is not integer deliver the first page
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    # if the page num is out of range, deliver the last page
    except EmptyPage:
        page_obj.number = paginator.get_page(1)
    # get highest & lowest price from articles
    agg_results = Article.objects.aggregate(max_price=Max(
        'wholesale_price'), min_price=Min('wholesale_price'))
    highest_price = int(agg_results['max_price'])
    # check if filter applied on articles
    filter_applied = False
    if len(all_articles) < len(Article.objects.all().values()):
        filter_applied = True
    # get cart object from request session
    cart = Cart(request)
    context = {
        'title': 'Shop',
        'page_obj': page_obj,  # send the selected objects for the page
        'brands': brands,  # send all brands
        'categories': categories,  # send all categories
        'form': form,  # send the form
        # send the seleced category if exist otherwise epmty string
        'selected_category': category_id if category_id else '',
        # send the seleced brand if exist otherwise epmty string
        'selected_brand': brand_id if brand_id else '',
        # send query
        'query': query,  
        'prp': articles_per_page,
        # get the highest possible price from articles
        'highest_price': highest_price,
        # send if filter is appllied
        'filter_applied': filter_applied,
        'cart': cart
    }
    return render(request, 'shopping/shop.html', context)

def article_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article_images = ArticleImage.objects.filter(article_id=article.id)
    context = {
        'title': f'{article.name.capitalize()} Details',
        'article': article,
        'article_images': article_images,
    }
    return render(request, 'shopping/article_details.html', context)

# define add product to cart view


def add_card(request):
    # get the cart object from the request session
    cart = Cart(request)
    # check if the request is POST
    if request.POST.get('action') == 'post':
        message = True
        message = ''
        article_id = request.POST.get('articleId')
        if not article_id:
            success = False
            message = 'Some thing whent wrong in fetching article !'
            return JsonResponse({'success': success, 'message': message})
        # if yes get & convert given ID
        article_id = int(request.POST.get('articleId'))
        # get article with request ID
        article = Article.objects.get(id=article_id)
        if not article.available:
            success = False
            message = f'Sorry, {article.name} currently not available !'
            return JsonResponse({'success': success, 'message': message})
        # get request quantity
        quantity = request.POST.get('quantity')
        # check if quantity != 0 or is request from articles list
        if quantity:
            # if yes convert quantity into integer
            int(quantity)
            # add article to cart with given article & quantity and set update quantity into True
            cart.add(article=article, quantity=quantity, update_quantity=True)
            success = True
            message = f'{article.name.capitalize()} Added To Your Bug'
        else:
            # else add article with default quantity (1)
            cart.add(article)
            success = True
            message = f'{article.name.capitalize()} Added To Your Bag'
    # return response with article name & lenght of cart
    return JsonResponse({'success': success, 'length': cart.__len__(), 'message': message})


def card_details(request):
    # get cart object from requst session
    cart = Cart(request)
    context = {
        'title': 'Cart Details',
        'cart': cart,
    }
    return render(request, 'shopping/card_details.html', context)
# define remove article from cart view


def card_remove(request, id):
    # get cart
    cart = Cart(request)
    # get product by ID
    article = get_object_or_404(Article, id=id)
    # remove product from cart
    cart.remove(article)
    # go to cart details page
    return redirect('shopping:card_details')

# define clear view


def clear_card(request):
    # get cart
    cart = Cart(request)
    # clear cart
    cart.clear()
    # go to home page
    return redirect('shopping:shop')
