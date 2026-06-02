from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.MyProfileView.as_view(), name='my_profile'),
    path('<int:user_id>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('users/<int:user_id>/follow/', views.FollowView.as_view(), name='follow_user'),
]