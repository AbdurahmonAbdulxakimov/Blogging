from rest_framework import serializers

from django.db.models import QuerySet

from posts.models import Post, Category, Tag
from users.api.serializers import UserDetailSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class PostSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "cover_image",
            "title",
            "content",
            "views_count",
            "user",
            "category",
            "tags",
            "status",
            "published_date",
            "created_at",
            "updated_at",
        )

class PostCreateSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    category = serializers.CharField(max_length=255)
    tags = serializers.CharField(max_length=255)

    class Meta:
        model = Post
        fields = (
            "id",
            "cover_image",
            "title",
            "content",
            "views_count",
            "user",
            "category",
            "tags",
            "status",
            "published_date",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        category: str = validated_data.pop('category')
        tags: str = validated_data.pop('tags')

        category, _ = Category.objects.get_or_create(title=category)

        tag_list = []
        for tag in tags.split(','):
            tag, _ = Tag.objects.get_or_create(title=tag)
            tag_list.append(tag)


        validated_data['category'] = category
        validated_data['tags'] = tag_list

        return validated_data

    def to_representation(self, instance):
        return PostSerializer(instance).data
