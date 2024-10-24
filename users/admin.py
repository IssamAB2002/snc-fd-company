from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(BaseUserAdmin):
    # Display these fields in the admin list view
    list_display = ('first_name', 'last_name', 'email',
                    'phone_number', 'is_superuser')
    # Filter by these fields in the admin list view
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    # Fieldsets for the admin change view
    fieldsets = (
        (None, {'fields': ('email', 'phone_number','first_name', 'last_name', 'state', 'city', 'street','sec_phone_number' , 'email_verified','phone_verified','password')}),  # Basic info
        ('Permissions', {'fields': ('is_staff', 'is_active',  # Permissions
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # Last login
    )

    # Fieldsets for the admin add view
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Wide layout
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}  # Add fields
         ),
    )

    # Search by these fields in the admin list view
    search_fields = ('email', 'first_name', 'last_name')

    # Default ordering in the admin list view
    ordering = ('first_name', 'last_name', 'email',)

    # Horizontal filter for these fields
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
