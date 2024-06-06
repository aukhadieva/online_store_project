from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'views_count',)
    search_fields = ('title', 'body',)
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
