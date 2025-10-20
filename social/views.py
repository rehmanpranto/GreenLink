from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Post, PostLike, PostReaction, Comment, Follow, Hashtag, Experience, 
    Education, Skill, UserSkill, Connection, StudyGroup, Notification,
    Story, Group, Event, FriendRequest, Friendship
)

User = get_user_model()

@login_required
def facebook_feed(request):
    """Modern Facebook-like feed with stories, posts, and sidebar content"""
    # Get posts from friends and followed users
    friends = get_user_friends(request.user)
    following_users = request.user.following.values_list('following', flat=True)
    all_connections = list(set(list(friends) + list(following_users)))
    
    posts = Post.objects.filter(
        Q(author__in=all_connections) | Q(author=request.user),
        is_public=True
    ).select_related('author').prefetch_related(
        'reactions', 'comments__author', 'tagged_users'
    ).order_by('-created_at')
    
    # Get active stories (last 24 hours)
    yesterday = timezone.now() - timedelta(hours=24)
    active_stories = Story.objects.filter(
        author__in=all_connections,
        created_at__gte=yesterday
    ).select_related('author').order_by('-created_at')
    
    # Friend requests
    friend_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related('sender').order_by('-created_at')[:5]
    
    # Online friends (simulate with recent activity)
    recent_active = timezone.now() - timedelta(minutes=30)
    online_friends = User.objects.filter(
        id__in=friends,
        last_active__gte=recent_active
    )[:10]
    
    # Upcoming events
    upcoming_events = Event.objects.filter(
        start_datetime__gte=timezone.now(),
        attendees=request.user
    ).order_by('start_datetime')[:5]
    
    # Suggested groups
    user_groups = request.user.joined_social_groups.values_list('id', flat=True)
    suggested_groups = Group.objects.exclude(
        id__in=user_groups
    ).filter(group_type='public').order_by('-members_count')[:5]
    
    # Pagination for posts
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Add user reaction info to posts
    for post in page_obj:
        try:
            user_reaction = post.reactions.filter(user=request.user).first()
            post.user_reaction_type = user_reaction.reaction_type if user_reaction else None
        except:
            post.user_reaction_type = None
    
    context = {
        'posts': page_obj,
        'active_stories': active_stories,
        'friend_requests': friend_requests,
        'online_friends': online_friends,
        'upcoming_events': upcoming_events,
        'suggested_groups': suggested_groups,
    }
    return render(request, 'social/facebook_feed.html', context)

def get_user_friends(user):
    """Get all friends of a user"""
    friendships1 = Friendship.objects.filter(user1=user).values_list('user2', flat=True)
    friendships2 = Friendship.objects.filter(user2=user).values_list('user1', flat=True)
    return list(set(list(friendships1) + list(friendships2)))

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'post')
        images = request.FILES.getlist('images')  # Handle multiple images
        
        if content or images:
            post = Post.objects.create(
                author=request.user,
                content=content,
                post_type=post_type
            )
            
            # Handle multiple images
            if images:
                image_urls = []
                for image in images:
                    # For now, just store the first image in the image field
                    if not post.image:
                        post.image = image
                        post.save()
                    # Store all image URLs in the images JSONField
                    image_urls.append(image.url if hasattr(image, 'url') else str(image))
                
                if image_urls:
                    post.images = image_urls
                    post.save()
            
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Post content cannot be empty.')
    
    return redirect('social:facebook_feed')

@login_required
def like_post(request, post_id):
    """Like/unlike a post (AJAX)"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            post.likes_count -= 1
            liked = False
        else:
            post.likes_count += 1
            liked = True
            
            # Create notification
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='like',
                    message=f'{request.user.get_display_name} liked your post'
                )
        
        post.save()
        
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def follow_user(request, user_id):
    """Follow/unfollow a user"""
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if user_to_follow == request.user:
            return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            follow.delete()
            request.user.following_count -= 1
            user_to_follow.followers_count -= 1
            following = False
        else:
            request.user.following_count += 1
            user_to_follow.followers_count += 1
            following = True
            
            # Create notification
            Notification.objects.create(
                recipient=user_to_follow,
                sender=request.user,
                notification_type='follow',
                message=f'{request.user.get_display_name} started following you'
            )
        
        request.user.save()
        user_to_follow.save()
        
        return JsonResponse({
            'following': following,
            'followers_count': user_to_follow.followers_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def professional_profile(request, user_id):
    """LinkedIn-like professional profile view"""
    profile_user = get_object_or_404(User, id=user_id)
    experiences = profile_user.experiences.all()
    education = profile_user.education.all()
    skills = UserSkill.objects.filter(user=profile_user).select_related('skill')
    
    # Check if users are connected
    is_connected = Connection.objects.filter(
        Q(sender=request.user, receiver=profile_user) |
        Q(sender=profile_user, receiver=request.user),
        status='accepted'
    ).exists()
    
    # Check for pending connection request
    pending_request = Connection.objects.filter(
        sender=request.user,
        receiver=profile_user,
        status='pending'
    ).exists()
    
    context = {
        'profile_user': profile_user,
        'experiences': experiences,
        'education': education,
        'skills': skills,
        'is_connected': is_connected,
        'pending_request': pending_request,
    }
    return render(request, 'social/professional_profile.html', context)

@login_required
def send_connection_request(request, user_id):
    """Send LinkedIn-like connection request"""
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=user_id)
        message = request.POST.get('message', '')
        
        if receiver == request.user:
            messages.error(request, 'Cannot connect with yourself.')
            return redirect('social:professional_profile', user_id=user_id)
        
        # Check if connection already exists
        existing_connection = Connection.objects.filter(
            Q(sender=request.user, receiver=receiver) |
            Q(sender=receiver, receiver=request.user)
        ).first()
        
        if existing_connection:
            messages.warning(request, 'Connection request already exists.')
        else:
            Connection.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message
            )
            
            # Create notification
            Notification.objects.create(
                recipient=receiver,
                sender=request.user,
                notification_type='connection',
                message=f'{request.user.get_display_name} sent you a connection request'
            )
            
            messages.success(request, 'Connection request sent successfully!')
    
    return redirect('social:professional_profile', user_id=user_id)

@login_required
def trending_hashtags(request):
    """View trending hashtags"""
    hashtags = Hashtag.objects.order_by('-usage_count')[:50]
    
    context = {
        'hashtags': hashtags,
    }
    return render(request, 'social/trending.html', context)

@login_required
def notifications(request):
    """View user notifications"""
    notifications = request.user.notifications.all()[:20]
    
    # Mark notifications as read
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'social/notifications.html', context)
