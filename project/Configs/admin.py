from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileetAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'language')
    list_filter = ('user', 'language')
    search_fields = ('user', 'language')
