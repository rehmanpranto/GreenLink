from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<uuid:post_id>/like/', views.like_post, name='like_post'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('profile/<int:user_id>/', views.professional_profile, name='professional_profile'),
    path('connect/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('groups/', views.study_groups, name='study_groups'),
    path('trending/', views.trending_hashtags, name='trending'),
    path('notifications/', views.notifications, name='notifications'),
]
