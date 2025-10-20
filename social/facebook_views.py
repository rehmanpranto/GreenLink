"""
Additional Facebook-style views for GreenLink
"""

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import models
from .models import Post, PostReaction, Comment, FriendRequest, Friendship
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
@require_POST
def react_to_post(request, post_id):
    """Handle Facebook-style reactions to posts"""
    try:
        post = get_object_or_404(Post, pk=post_id)
        data = json.loads(request.body)
        reaction_type = data.get('reaction_type', 'like')
        
        # Remove existing reaction if any
        PostReaction.objects.filter(user=request.user, post=post).delete()
        
        # Add new reaction
        PostReaction.objects.create(
            user=request.user,
            post=post,
            reaction_type=reaction_type
        )
        
        # Update post reaction counts
        post.update_reaction_counts()
        
        return JsonResponse({
            'success': True,
            'reaction_type': reaction_type,
            'total_reactions': sum(post.reactions_count.values()) if post.reactions_count else 0
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def add_comment(request, post_id):
    """Add a comment to a post"""
    try:
        post = get_object_or_404(Post, pk=post_id)
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        # Update post comment count
        post.comments_count = post.comments.count()
        post.save(update_fields=['comments_count'])
        
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'author_name': comment.author.get_display_name,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%b %d, %Y at %I:%M %p')
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def accept_friend_request(request, request_id):
    """Accept a friend request"""
    try:
        friend_request = get_object_or_404(
            FriendRequest, 
            pk=request_id, 
            receiver=request.user,
            status='pending'
        )
        
        # Update request status
        friend_request.status = 'accepted'
        friend_request.save()
        
        # Create friendship
        Friendship.objects.get_or_create(
            user1=friend_request.sender,
            user2=friend_request.receiver
        )
        
        return JsonResponse({
            'success': True,
            'message': f'You are now friends with {friend_request.sender.get_display_name}'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def decline_friend_request(request, request_id):
    """Decline a friend request"""
    try:
        friend_request = get_object_or_404(
            FriendRequest, 
            pk=request_id, 
            receiver=request.user,
            status='pending'
        )
        
        friend_request.status = 'declined'
        friend_request.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Friend request declined'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def create_story(request):
    """Create a new story"""
    if request.method == 'POST':
        # Handle story creation
        pass
    return render(request, 'social/create_story.html')

@login_required
def groups_list(request):
    """List all groups"""
    from .models import Group
    groups = Group.objects.filter(group_type='public').order_by('-members_count')
    return render(request, 'social/groups_list.html', {'groups': groups})

@login_required
def friends_list(request):
    """List user's friends"""
    # Get user's friends from Friendship model
    from .models import Friendship
    friendships = Friendship.objects.filter(
        models.Q(user1=request.user) | models.Q(user2=request.user)
    )
    
    friend_ids = []
    for friendship in friendships:
        if friendship.user1 == request.user:
            friend_ids.append(friendship.user2.id)
        else:
            friend_ids.append(friendship.user1.id)
    
    friends_users = User.objects.filter(id__in=friend_ids)
    return render(request, 'social/friends_list.html', {'friends': friends_users})

@login_required
def find_friends(request):
    """Find and suggest friends"""
    # Get current friends
    friendships = Friendship.objects.filter(
        models.Q(user1=request.user) | models.Q(user2=request.user)
    )
    
    current_friend_ids = []
    for friendship in friendships:
        if friendship.user1 == request.user:
            current_friend_ids.append(friendship.user2.id)
        else:
            current_friend_ids.append(friendship.user1.id)
    
    # Get users who are not friends yet
    suggested_users = User.objects.exclude(
        id__in=current_friend_ids
    ).exclude(id=request.user.id)[:20]
    
    return render(request, 'social/find_friends.html', {'suggested_users': suggested_users})

@login_required
def marketplace(request):
    """Marketplace view for buying/selling items"""
    return render(request, 'social/marketplace.html')

@login_required
def memories(request):
    """Memories/timeline view"""
    return render(request, 'social/memories.html')
