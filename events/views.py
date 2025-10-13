from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def events_list(request):
    """Display events list for the authenticated user"""
    return render(request, 'events/events_list.html')
