from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import CustomUser, StudentVerification
from .forms import GreenUniversityRegistrationForm, GreenUniversityLoginForm
import random
import string


class GreenUniversityLoginView(LoginView):
    """Custom login view for Green University students"""
    template_name = 'accounts/login.html'
    form_class = GreenUniversityLoginForm
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Green University of Bangladesh'
        context['page_title'] = 'Student Login - Green University'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back to GreenLink!')
        return super().form_valid(form)


class GreenUniversityRegistrationView(CreateView):
    """Registration view for new Green University students"""
    model = CustomUser
    form_class = GreenUniversityRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Green University of Bangladesh'
        context['page_title'] = 'Join GreenLink'
        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Require email verification
        user.save()
        
        # Create verification code
        verification_code = ''.join(random.choices(string.digits, k=6))
        StudentVerification.objects.create(
            user=user,
            verification_code=verification_code
        )
        
        messages.success(
            self.request, 
            f'Registration successful! Please check your Green University email for verification.'
        )
        
        return super().form_valid(form)


def verify_email(request, user_id, code):
    """Verify student email address"""
    try:
        user = CustomUser.objects.get(id=user_id)
        verification = StudentVerification.objects.get(
            user=user, 
            verification_code=code, 
            is_used=False
        )
        
        user.is_active = True
        user.is_verified = True
        user.save()
        
        verification.is_used = True
        verification.save()
        
        messages.success(request, 'Email verified successfully! You can now login.')
        return redirect('accounts:login')
        
    except (CustomUser.DoesNotExist, StudentVerification.DoesNotExist):
        messages.error(request, 'Invalid verification link.')
        return redirect('accounts:register')


@login_required
def profile_setup(request):
    """Complete profile setup after registration"""
    if request.method == 'POST':
        user = request.user
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        if 'bio' in request.POST:
            user.bio = request.POST['bio']
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profiles:dashboard')
    
    return render(request, 'accounts/profile_setup.html', {
        'user': request.user,
        'university_name': 'Green University of Bangladesh'
    })
