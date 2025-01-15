from django.contrib import admin
from .models import FriendlySent, Follow

# Registra el modelo para verlo en el admin
@admin.register(FriendlySent)
class FriendlySentAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('from_user__username', 'to_user__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(qs)  # Imprime los registros en la consola
        return qs

@admin.register(Follow)
class FollowSetAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('follower', 'following')
    search_fields = ('follower', 'following')
