from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "created", "title"]
    date_hierarchy = "created"
    filter_horizontal = ["likes", "unlikes"]
    readonly_fields = ["created", "edited"]


admin.site.register(Post, PostAdmin)
