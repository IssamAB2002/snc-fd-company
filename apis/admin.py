from django.contrib import admin
from .models import AndroidApp

@admin.register(AndroidApp)
class AndroidAppAdmin(admin.ModelAdmin):
    list_display = ('version', 'uploaded_at')