from django.contrib.auth.forms import UserChangeForm, UsernameField
from .models import User


class UserAdminForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}
