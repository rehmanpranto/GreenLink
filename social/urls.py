from django.urls import path
from . import views
from . import facebook_views

app_name = 'social'

urlpatterns = [
    path('', views.facebook_feed, name='feed'),  # Make Facebook feed the default
    path('facebook/', views.facebook_feed, name='facebook_feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<uuid:post_id>/like/', views.like_post, name='like_post'),
    
    # Facebook-style interactions
    path('react/<uuid:post_id>/', facebook_views.react_to_post, name='react_to_post'),
    path('comment/<uuid:post_id>/', facebook_views.add_comment, name='add_comment'),
    path('friend-request/<int:request_id>/accept/', facebook_views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/<int:request_id>/decline/', facebook_views.decline_friend_request, name='decline_friend_request'),
    
    # Additional pages
    path('create-story/', facebook_views.create_story, name='create_story'),
    path('groups/', facebook_views.groups_list, name='groups'),
    path('friends/', facebook_views.friends_list, name='friends'),
    path('find-friends/', facebook_views.find_friends, name='find_friends'),
    path('marketplace/', facebook_views.marketplace, name='marketplace'),
    path('memories/', facebook_views.memories, name='memories'),
    
    # Original views
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('profile/<int:user_id>/', views.professional_profile, name='professional_profile'),
    path('connect/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('trending/', views.trending_hashtags, name='trending'),
    path('notifications/', views.notifications, name='notifications'),
]
