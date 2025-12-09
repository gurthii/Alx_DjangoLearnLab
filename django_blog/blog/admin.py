from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)
    readonly_fields = ('published_date',)
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'content', 'author')
        }),
        ('Publication', {
            'fields': ('published_date',)
        }),
    )


admin.site.register(Post, PostAdmin)
