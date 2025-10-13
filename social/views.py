from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    Post, PostLike, Comment, Follow, Hashtag, Experience, 
    Education, Skill, UserSkill, Connection, StudyGroup, Notification
)

User = get_user_model()

@login_required
def feed(request):
    """Display social feed with Twitter-like posts"""
    # Get posts from followed users and own posts
    following_users = request.user.following.values_list('following', flat=True)
    posts = Post.objects.filter(
        Q(author__in=following_users) | Q(author=request.user),
        is_public=True
    ).select_related('author').prefetch_related('likes', 'comments')
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Trending hashtags
    trending_hashtags = Hashtag.objects.order_by('-usage_count')[:10]
    
    # Suggested connections
    suggested_users = User.objects.exclude(
        id__in=following_users
    ).exclude(id=request.user.id)[:5]
    
    context = {
        'posts': page_obj,
        'trending_hashtags': trending_hashtags,
        'suggested_users': suggested_users,
    }
    return render(request, 'social/feed.html', context)

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'post')
        image = request.FILES.get('image')
        
        if content:
            post = Post.objects.create(
                author=request.user,
                content=content,
                post_type=post_type,
                image=image
            )
            
            # Update user's post count
            request.user.posts_count += 1
            request.user.save()
            
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Post content cannot be empty.')
    
    return redirect('social:feed')

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
def study_groups(request):
    """View and manage study groups"""
    groups = StudyGroup.objects.filter(is_public=True).order_by('-created_at')
    my_groups = request.user.study_groups.all()
    
    context = {
        'groups': groups,
        'my_groups': my_groups,
    }
    return render(request, 'social/study_groups.html', context)

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
