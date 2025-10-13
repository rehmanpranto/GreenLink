from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser

@login_required
def dashboard(request):
    """Main dashboard for students"""
    return render(request, 'profiles/dashboard.html', {
        'user': request.user,
        'university_name': 'Green University of Bangladesh'
    })

@login_required  
def profile_detail(request, pk):
    """View student profile"""
    user = CustomUser.objects.get(pk=pk)
    return render(request, 'profiles/profile_detail.html', {
        'profile_user': user,
        'university_name': 'Green University of Bangladesh'
    })

@login_required
def profile_edit(request):
    """Edit profile"""
    if request.method == 'POST':
        messages.success(request, 'Profile updated successfully!')
        return redirect('profiles:dashboard')
    
    return render(request, 'profiles/profile_edit.html', {
        'user': request.user,
        'university_name': 'Green University of Bangladesh'
    })
