from django.contrib import admin
from .models import BannerArticle, ContactMessage

admin.site.register(BannerArticle)
class ContactMessageAdmin(admin.ModelAdmin):
    ordering = ('-created_at', 'subject')
admin.site.register(ContactMessage, ContactMessageAdmin)