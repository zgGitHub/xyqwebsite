from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','avatar','role','is_active')
    list_filter = ('role',)