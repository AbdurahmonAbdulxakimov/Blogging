from django.urls import path

from posts import views


app_name = 'posts'

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='post-list'),
    path('newest/', views.NewestPostListAPIView.as_view(), name='newest-post-list'),
    path('popular/', views.PopularPostListAPIView.as_view(), name='popular-post-list'),
    path('months-popular/', views.MonthsPopularPostListAPIView.as_view(), name='months-popular-post-list'),
    path('weeks-popular/', views.WeeksPopularPostListAPIView.as_view(), name='weeks-popular-post-list'),
    path('create/', views.PostCreateAPIView.as_view(), name='post-create'),
    path('detail/<int:pk>/', views.PostDetailAPIView.as_view(), name='post-create'),
]
