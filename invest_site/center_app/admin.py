from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import *


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', )
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields = ('email',)
    ordering = ('email',)

    filter_horizontal = ()


class MyUserAdmin(UserAdmin):
    pass


admin.site.register(MyUser, MyUserAdmin)
