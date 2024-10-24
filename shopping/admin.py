from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, SubCategory, ArticleImage,Brand, Article
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ArticleImage)
admin.site.register(Brand)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'wholesale_price', 'available')
    fieldsets = ((None, {'fields': ('name', 'subcategory', 'slug',
                 'description', 'extra_description', 'wholesale_price', 'detail_price', 'available', 'brand', 'specification', 'images', 'video', 'discounted_price', 'deal_end_time')}),)
    search_fields = ('name', 'description')
admin.site.register(Article, ArticleAdmin)
