from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),
    path('comments/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('posts/<int:post_id>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('comments/<int:comment_id>/like/', views.CommentLikeView.as_view(), name='comment_like'),
]