from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import re


class CustomUser(AbstractUser):
    """Custom user model for Green University students"""
    
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('EEE', 'Electrical & Electronic Engineering'),
        ('CE', 'Civil Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('BBA', 'Bachelor of Business Administration'),
        ('ENG', 'English'),
        ('LAW', 'Law'),
        ('ARCH', 'Architecture'),
        ('PHARM', 'Pharmacy'),
        ('TEX', 'Textile Engineering'),
    ]
    
    @classmethod
    def get_batch_choices(cls):
        """Generate batch choices dynamically from 2003 to current year + 1"""
        from datetime import datetime
        current_year = datetime.now().year
        choices = []
        
        # Generate from current year + 1 down to 2003 (most recent first)
        for year in range(current_year + 1, 2002, -1):
            choices.extend([
                (f'Fall {year}', f'Fall {year}'),
                (f'Summer {year}', f'Summer {year}'),
                (f'Spring {year}', f'Spring {year}'),
            ])
        
        return choices
    
    BATCH_CHOICES = []  # Will be populated dynamically
    
    # Green University email validation
    email = models.EmailField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{9}@student\.green\.ac\.bd$',
                message='Must be a valid Green University email (format: 123456789@student.green.ac.bd)'
            )
        ]
    )
    
    student_id = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{9}$',
                message='Student ID must be exactly 9 digits'
            )
        ],
        help_text="9-digit Green University student ID"
    )
    
    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES,
        help_text="Your academic department"
    )
    
    batch = models.CharField(
        max_length=20,
        help_text="Your admission batch (e.g., Fall 2023, Spring 2024)"
    )
    
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?880\d{10}$|^\d{11}$',
                message='Enter a valid Bangladeshi phone number'
            )
        ]
    )
    
    is_verified = models.BooleanField(default=False, help_text="Email verification status")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # LinkedIn-like professional fields
    headline = models.CharField(max_length=220, blank=True, help_text="Professional headline")
    location = models.CharField(max_length=100, blank=True, help_text="Current location")
    website = models.URLField(blank=True, help_text="Personal website or portfolio")
    github_username = models.CharField(max_length=39, blank=True, help_text="GitHub username")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    
    # Academic fields
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    interests = models.TextField(max_length=500, blank=True, help_text="Academic and career interests")
    
    # Twitter-like fields
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'student_id', 'department', 'batch']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Green University Student'
        verbose_name_plural = 'Green University Students'
    
    def save(self, *args, **kwargs):
        # Auto-generate username from student ID if not provided
        if not self.username:
            self.username = self.student_id
        
        # Ensure email matches student ID
        if self.student_id and not self.email.startswith(self.student_id):
            if not self.email:
                self.email = f"{self.student_id}@student.green.ac.bd"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.student_id})"
    
    @property
    def get_display_name(self):
        return self.get_full_name() or self.username
    
    @property
    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default-avatar.svg'


class StudentVerification(models.Model):
    """Model to handle student verification process"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification')
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'student_verification'
    
    def __str__(self):
        return f"Verification for {self.user.student_id}"
