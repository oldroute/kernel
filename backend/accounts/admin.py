from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserAdminForm


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': (
            'email', 'avatar', 'first_name', 'last_name', 'password'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    form = UserAdminForm


admin.site.register(User, CustomUserAdmin)