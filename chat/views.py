from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q, Max
from .models import Conversation, Message

User = get_user_model()


@login_required
def chat_list(request):
    """Display chat list for the authenticated user"""
    # Get all conversations for the current user
    conversations = request.user.conversations.all().annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')
    
    # Prepare conversation data
    conversation_data = []
    for conv in conversations:
        other_user = conv.get_other_participant(request.user)
        last_message = conv.get_last_message()
        
        if other_user and last_message:
            conversation_data.append({
                'id': conv.id,
                'other_user': other_user,
                'last_message': last_message,
                'unread_count': conv.messages.filter(is_read=False).exclude(sender=request.user).count()
            })
    
    context = {
        'conversations': conversation_data,
    }
    return render(request, 'chat/chat_list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Display a specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is a participant
    if request.user not in conversation.participants.all():
        return redirect('chat:chat_list')
    
    # Mark all messages in this conversation as read
    conversation.messages.exclude(sender=request.user).update(is_read=True)
    
    # Get all messages
    messages = conversation.messages.all()
    other_user = conversation.get_other_participant(request.user)
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
    }
    return render(request, 'chat/conversation_detail.html', context)


@login_required
def send_message(request, conversation_id):
    """Send a message in a conversation"""
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Check if user is a participant
        if request.user not in conversation.participants.all():
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'timestamp': message.timestamp.strftime('%I:%M %p'),
                    'sender': message.sender.username
                }
            })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def start_conversation(request, user_id):
    """Start a new conversation with a user"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Check if conversation already exists
    existing_conv = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_conv:
        return redirect('chat:conversation_detail', conversation_id=existing_conv.id)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    
    return redirect('chat:conversation_detail', conversation_id=conversation.id)
