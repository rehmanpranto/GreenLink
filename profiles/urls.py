from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('edit/', views.profile_edit, name='profile_edit'),
]
