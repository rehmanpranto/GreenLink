from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
import re


class GreenUniversityRegistrationForm(UserCreationForm):
    """Registration form for Green University students"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    student_id = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456789',
            'pattern': '[0-9]{9}',
            'title': 'Student ID must be exactly 9 digits'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '123456789@student.green.edu.bd'
        })
    )
    
    department = forms.ChoiceField(
        choices=CustomUser.DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Separate fields for batch selection (cleaner UI)
    batch_year = forms.ChoiceField(
        label="Admission Year",
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select your year of admission"
    )
    
    batch_semester = forms.ChoiceField(
        choices=[
            ('Spring', 'Spring (January–April)'),
            ('Summer', 'Summer (May–August)'),
            ('Fall', 'Fall (September–December)'),
        ],
        label="Semester",
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select your admission semester"
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+8801XXXXXXXXX or 01XXXXXXXXX'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'student_id', 'email', 'department', 'batch_year', 'batch_semester', 'phone_number', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Generate year choices dynamically (current year + 1 down to 2003)
        from datetime import datetime
        current_year = datetime.now().year
        year_choices = [(str(year), str(year)) for year in range(current_year + 1, 2002, -1)]
        self.fields['batch_year'].choices = year_choices
        
        # Set intelligent defaults
        self.fields['batch_year'].initial = str(current_year)
        
        current_month = datetime.now().month
        if current_month <= 4:
            default_semester = 'Spring'
        elif current_month <= 8:
            default_semester = 'Summer'
        else:
            default_semester = 'Fall'
        self.fields['batch_semester'].initial = default_semester
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        
        if not re.match(r'^\d{9}$', student_id):
            raise ValidationError('Student ID must be exactly 9 digits.')
        
        if CustomUser.objects.filter(student_id=student_id).exists():
            raise ValidationError('This student ID is already registered.')
        
        return student_id
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        student_id = self.cleaned_data.get('student_id')
        
        # Check if email follows Green University format
        if not re.match(r'^\d{9}@(student\.)?green\.edu\.bd$', email):
            raise ValidationError('Email must be in Green University format (123456789@student.green.edu.bd)')
        
        # Check if email matches student ID
        if student_id and not email.startswith(student_id):
            raise ValidationError('Email must start with your student ID.')
        
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            if not re.match(r'^\+?880\d{10}$|^\d{11}$', phone):
                raise ValidationError('Enter a valid Bangladeshi phone number.')
        return phone
    
    def save(self, commit=True):
        """Override save to combine batch_year and batch_semester into batch field"""
        user = super().save(commit=False)
        
        # Combine year and semester into batch field
        batch_year = self.cleaned_data['batch_year']
        batch_semester = self.cleaned_data['batch_semester']
        user.batch = f"{batch_semester} {batch_year}"
        
        if commit:
            user.save()
        return user


class GreenUniversityLoginForm(AuthenticationForm):
    """Login form for Green University students"""
    
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Green University email',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check if it's a Green University email
        if not re.match(r'^\d{9}@(student\.)?green\.edu\.bd$', username):
            raise ValidationError('Please use your Green University email address.')
        
        return username


class ProfileUpdateForm(forms.ModelForm):
    """Form to update student profile"""
    
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us about yourself...'
        })
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+8801XXXXXXXXX'
        })
    )
    
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'phone_number', 'profile_picture']
