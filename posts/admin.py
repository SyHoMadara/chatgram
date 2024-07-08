from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'receiver', 'message', 'created_at', 'edited_at')
    search_fields = ('author', 'receiver', 'message')
    list_filter = ('created_at', 'edited_at')


admin.site.register(Post, PostAdmin)
