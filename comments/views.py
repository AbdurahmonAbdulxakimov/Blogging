from rest_framework.generics import CreateAPIView, ListAPIView

from comments.serializers import CommentCreateSerializer, CommentSerializer
from comments.models import Comment

class CommentCreateView(CreateAPIView):
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', None)
        print(post_id)
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.none()
