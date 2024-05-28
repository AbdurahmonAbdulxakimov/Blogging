from django.contrib import admin

from posts.models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status")
    list_display_links = ("id", "title")




