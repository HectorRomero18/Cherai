from django.contrib import admin
from .models import Notification

# Register your models here.
@admin.register(Notification)
class NotificationSetAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'created_at')
