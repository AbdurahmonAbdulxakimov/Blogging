from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', "comment_obj")
    list_display_links = ("id", "comment_obj")

    def get_queryset(self, request):
        qs = Comment.objects.all().select_related("user", "post")
        return qs

    def comment_obj(self, obj):
        return obj.user.username + ' | ' + obj.post.title
