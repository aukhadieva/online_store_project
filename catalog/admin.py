from django.contrib import admin

from catalog.models import Product, Category, Contact, BlogPost


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'category',)
    search_fields = ('product_name', 'prod_desc',)
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message',)
    search_fields = ('message',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'views_count',)
    search_fields = ('title', 'body',)
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
