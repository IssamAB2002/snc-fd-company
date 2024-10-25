from django.db import models
from django.db.models import QuerySet 
from django.utils import timezone
from cloudinary.models import CloudinaryField

# create category model
class Category(models.Model):
    name = models.CharField(max_length=55, unique=True)
    slug = models.SlugField(max_length=55, unique=True)
    image = models.ImageField(
        upload_to='category_images', blank=True, null=True)

    def __str__(self):
        return self.name

# create subcategory model
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# create article images model
class ArticleImage(models.Model):
    image = CloudinaryField('images')
    article_id = models.ForeignKey(
        'Article', on_delete=models.CASCADE, related_name='article_images')
    
    def __str__(self):
        return f'{self.article_id.name} Image {self.pk}'

# create brand model
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True,
                                   null=True)

    logo = models.ImageField(upload_to='brand_logos', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
# create article specification
class ArticleSpecification(models.Model):
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    heigth = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    colors = models.CharField(max_length=55, null=True, blank=True)
    power = models.IntegerField()
    each_box_contains = models.IntegerField()

# create article model
class Article(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    extra_description = models.TextField(null=True, blank=True)
    wholesale_price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    detail_price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)
    specification = models.ForeignKey(ArticleSpecification, on_delete=models.CASCADE, null=True, blank=True)
    images = models.ManyToManyField(ArticleImage, blank=True)
    video = models.FileField(upload_to='product_videos', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    # sold settings
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    deal_end_time = models.DateTimeField(null=True, blank=True)

    def is_deal_active(self):
        if self.deal_end_time is not None:
            return timezone.now() < self.deal_end_time
        else:
            return False

    def __str__(self):
        return self.name


