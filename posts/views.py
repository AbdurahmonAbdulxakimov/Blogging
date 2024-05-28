from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from django.utils import timezone
from datetime import timedelta
from django.db import models

from posts.models import Post, Category, Tag, Status, PostViews
from posts.serializers import PostSerializer, PostCreateSerializer, CategorySerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.filter(status=Status.ACCEPTED)
    serializer_class = PostSerializer


class NewestPostListAPIView(ListAPIView):
    queryset = Post.objects.filter(status=Status.ACCEPTED).order_by('-published_date')[:7]
    serializer_class = PostSerializer


class PopularPostListAPIView(ListAPIView):
    queryset = Post.objects.filter(status=Status.ACCEPTED).order_by('-views_count')[:7]
    serializer_class = PostSerializer


class MonthsPopularPostListAPIView(ListAPIView):
    queryset = Post.objects.filter(status=Status.ACCEPTED)
    serializer_class = PostSerializer

    def get_queryset(self):
        month = timezone.now().month
        qs = self.queryset.annotate(months_views_count=models.Count(models.Subquery(
                     PostViews.objects.filter(created_at__month=month, post=models.OuterRef('id')).values_list("id", flat=True)
                    ))
                 ).order_by('-months_views_count')[:7]

        return qs


class WeeksPopularPostListAPIView(ListAPIView):
    queryset = Post.objects.filter(status=Status.ACCEPTED)
    serializer_class = PostSerializer

    def get_queryset(self):
        week_ago = timezone.now() - timedelta(days=7)
        qs = self.queryset.annotate(months_views_count=models.Count(models.Subquery(
                     PostViews.objects.filter(created_at__gte=week_ago, post=models.OuterRef('id')).values_list("id", flat=True)
                    ))
                 ).order_by('-months_views_count')[:7]

        return qs


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.filter(status=Status.ACCEPTED)
    serializer_class = PostSerializer

    def get_object(self):
        obj = super().get_object()
        PostViews.objects.get_or_create(user=self.request.user, ip=self.request.META['REMOTE_ADDR'], post=obj)
        return obj


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
