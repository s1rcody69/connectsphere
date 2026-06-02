from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post_list_create'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('user/<int:user_id>/', views.UserPostsView.as_view(), name='user_posts'),
]