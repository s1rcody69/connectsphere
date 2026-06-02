from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserSearchView.as_view(), name='user_search'),
]