from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from accounts.models import CustomUser

class LandingPageView(TemplateView):
    """Beautiful landing page for GreenLink"""
    template_name = 'home/landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get some statistics for the landing page
        total_students = CustomUser.objects.filter(is_active=True).count()
        context.update({
            'total_students': total_students,
            'total_departments': 15,  # You can make this dynamic later
            'total_posts': 2847,  # You can make this dynamic later
            'total_events': 156,  # You can make this dynamic later
        })
        
        return context

def home_view(request):
    """Simple home view function"""
    if request.user.is_authenticated:
        # Redirect authenticated users to dashboard
        from django.shortcuts import redirect
        return redirect('profiles:dashboard')
    
    # Show landing page for non-authenticated users
    return render(request, 'home/landing.html', {
        'total_students': CustomUser.objects.filter(is_active=True).count(),
        'total_departments': 15,
        'total_posts': 2847,
        'total_events': 156,
    })
