from django.conf import settings
from .models import Article
# import decimal converter
from decimal import Decimal
# create Cart model (object of article & infos which session will contain)


class Cart:
    # define cart, using the request object
    def __init__(self, request):
        # define cart session = the session sent with request
        self.session = request.session
        # define the cart as the session with the id in settings
        cart = self.session.get(settings.SESSION_CART_ID)
        # if there's not a session with the specific session id the create one
        if not cart:
            # set the cart session with setting session id to empty dict
            cart = self.session[settings.SESSION_CART_ID] = {}
        # set the cart object available to all website pages
        self.cart = cart

    # define the add function (with params obj_self, article, quantity default 1, update quantity defauld to false)
    def add(self, article, quantity=1, update_quantity=False):
        # get the article id
        article_id = str(article.id)
        if article.is_deal_active():
            price = str(article.discounted_price)
        else: 
            price = str(article.wholesale_price)
        # get & convert the quantity into integer
        quantity = int(quantity)
        # check if there's not obj with getted id in cart
        if article_id not in self.cart:
            # if not add it to cart 
            self.cart[article_id] = {
                'quantity': 0, 'price': price}
        # check if request for update quantity
        if update_quantity:
            # if yes set the quantity to the given quantity
            self.cart[article_id]['quantity'] = quantity
        else:
            # else convert quantity into integer
            int(quantity)
            # add it to the previous quantity(0, or with list add)
            self.cart[article_id]['quantity'] += quantity
        # save cart
        self.save()

    # define save function
    def save(self):
        # set session to modified
        self.session.modified = True
    # define get quantity function

    def get_quantity(self, article):
        # get & convert article id into str
        article_id = str(article.id)
        # check if there's obj with article id
        if self.cart[article_id]:
            # if yes return quantity of the article
            return self.cart[article_id]['quantity']
        else:
            # else return 0
            return 0
    # define remove function

    def remove(self, article):
        # get & convert article id into str
        article_id = str(article.id)
        # check if there's article id in cart
        if article_id in self.cart:
            # if yes delete the article id obj from cart
            del self.cart[article_id]
            # save cart
            self.save()
    # define iterate function

    def __iter__(self):
        # ket all the IDs from the cart (keys)
        article_ids = self.cart.keys()
        # get all the articles included in cart (by there IDs)
        articles = Article.objects.filter(id__in=article_ids)
        # make a copy of cart
        cart = self.cart.copy()
        # loop over the filtered articles (each id = obj)
        for article in articles:
            # each article set key article into article obj
            cart[str(article.id)]['article'] = article
            # set key price to the price
            cart[str(article.id)]['price'] = Decimal(
                cart[str(article.id)]['price'])  # Convert price to Decimal
            # set key quantity to converted quantity (to str)
            cart[str(article.id)]['quantity'] = int(
                cart[str(article.id)]['quantity'])
            # set key total price into total price from cart
            cart[str(article.id)]['total_price'] = cart[str(article.id)
                                                        ]['price'] * cart[str(article.id)]['quantity']
            # return the created object
            yield cart[str(article.id)]
    # define lenght of cart function

    def __len__(self):
        # return length
        return len(self.cart)
    # define total price function

    def get_total_price(self):
        # get the th sum of multiplation price x quantity for each obj in cart
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    # define clear function

    def clear(self):
        # clear all the cart object in session
        del self.session[settings.SESSION_CART_ID]
        # save session
        self.save()
