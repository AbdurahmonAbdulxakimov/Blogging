from django.db.models import Q
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        SerializerMethodField)
from rest_framework.utils.serializer_helpers import ReturnDict

from users.api.serializers import UserDetailSerializer
from comments.models import Comment


class CommentSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    children = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "content", "user", "children", "created_at", "updated_at",)

    def get_children(self, obj: Comment) -> ReturnDict:
        user = self.context["request"].user
        if user and user.is_authenticated:
            return CommentChildModelSerializer(
                obj.children.filter(user=user),
                many=True, context=self.context
            ).data
        return CommentChildModelSerializer(obj.children.all(), many=True).data


class CommentChildModelSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id", "content", "user", "created_at", "updated_at",)


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "parent",
            "user",
            "post",
            "content",
        )
        read_only_fields = ("id", "user")

    def create(self, validated_data):
        parent = validated_data.pop("parent", None)
        comment = Comment.objects.create(**validated_data)

        # Check if a parent exists
        if parent:
            # Check if the parent has a parent itself
            if not parent.parent:
                # If not, assign the parent directly to the comment's parent attribute
                comment.parent = parent
            else:
                # If the parent has a parent, assign the parent's parent to the comment's parent attribute
                comment.parent = parent.parent

        comment.save()
        return comment

    def to_representation(self, instance) -> dict:
        comment = super().to_representation(instance)
        comment["parent"] = CommentChildModelSerializer(instance.parent, context=self.context).data if instance.parent else None
        return comment
