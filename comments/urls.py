from django.urls import path

from comments import views


app_name = 'comments'

urlpatterns = [
    path('<int:post_id>/', views.CommentListView.as_view(), name='comment-list'),
    path('create/', views.CommentCreateView.as_view(), name='comment-create'),
]
