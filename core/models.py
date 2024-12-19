from django.db import models
from users.models import User
from shopping.models import Article

class BannerArticle(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    article = models.ForeignKey(
        Article, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='banner_article_imgs/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.last_name} {self.subject}'
