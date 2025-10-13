from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_list(request):
    """Display chat list for the authenticated user"""
    return render(request, 'chat/chat_list.html')
