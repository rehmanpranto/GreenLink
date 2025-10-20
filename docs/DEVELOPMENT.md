# GreenLink Development Guide

## 🚀 Getting Started with Development

This guide provides comprehensive instructions for developers working on GreenLink, including setup, coding standards, and contribution guidelines.

## 🛠️ Development Environment Setup

### Prerequisites
- **Python 3.8+** (Recommended: Python 3.11+)
- **Git** version control
- **Code Editor** (Recommended: VS Code with Python extension)
- **Virtual Environment** (venv or conda)

### Initial Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/rehmanpranto/GreenLink.git
   cd GreenLink
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser  # Optional
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure Deep Dive

### Directory Organization
```
GreenLink/
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── DEVELOPMENT.md
├── green_university_campus/        # Main Django project
│   ├── __init__.py
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py                     # WSGI config
│   └── asgi.py                     # ASGI config (future WebSocket)
├── accounts/                       # User authentication app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py                    # Admin interface config
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Authentication forms
│   ├── models.py                   # User models
│   ├── urls.py                     # App URL patterns
│   └── views.py                    # Authentication views
├── profiles/                       # User profiles app
├── social/                         # Social networking app
├── chat/                          # Messaging system app
├── events/                        # Event management app
├── home/                          # Landing pages app
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   ├── components/                # Reusable components
│   ├── accounts/                  # Auth templates
│   ├── profiles/                  # Profile templates
│   ├── social/                    # Social templates
│   ├── chat/                      # Chat templates
│   ├── events/                    # Event templates
│   └── home/                      # Home templates
├── static/                        # Static files
│   ├── css/
│   │   └── green_university.css   # Main stylesheet
│   ├── js/                        # JavaScript files
│   ├── images/                    # Image assets
│   └── icons/                     # Icon files
├── media/                         # User uploaded files
├── requirements.txt               # Python dependencies
├── manage.py                      # Django management script
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
└── README.md                      # Project overview
```

## 🎨 Coding Standards

### Python Code Style (PEP 8)

1. **Import Organization**
   ```python
   # Standard library imports
   import os
   import sys
   
   # Third-party imports
   from django.shortcuts import render
   from django.contrib.auth import authenticate
   
   # Local application imports
   from .models import CustomUser
   from .forms import RegistrationForm
   ```

2. **Function and Class Naming**
   ```python
   # Functions: snake_case
   def create_user_profile(user, department):
       pass
   
   # Classes: PascalCase
   class CustomUserManager(BaseUserManager):
       pass
   
   # Constants: UPPER_CASE
   MAX_POST_LENGTH = 2200
   ```

3. **Docstrings and Comments**
   ```python
   def validate_student_email(email):
       """
       Validate Green University student email format.
       
       Args:
           email (str): Email address to validate
           
       Returns:
           bool: True if valid, False otherwise
           
       Example:
           >>> validate_student_email("123456789@student.green.edu.bd")
           True
       """
       import re
       pattern = r'^\d{9}@student\.green\.edu\.bd$'
       return bool(re.match(pattern, email))
   ```

### Django Best Practices

1. **Model Design**
   ```python
   class Post(models.Model):
       """Social media post model."""
       
       author = models.ForeignKey(
           'accounts.CustomUser',
           on_delete=models.CASCADE,
           related_name='posts'
       )
       content = models.TextField(max_length=2200)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       
       class Meta:
           ordering = ['-created_at']
           indexes = [
               models.Index(fields=['author', '-created_at']),
           ]
       
       def __str__(self):
           return f"{self.author.username} - {self.content[:50]}"
   ```

2. **View Organization**
   ```python
   from django.contrib.auth.decorators import login_required
   from django.utils.decorators import method_decorator
   from django.views.generic import ListView
   
   @method_decorator(login_required, name='dispatch')
   class SocialFeedView(ListView):
       """Display social feed for authenticated users."""
       
       model = Post
       template_name = 'social/feed.html'
       context_object_name = 'posts'
       paginate_by = 10
       
       def get_queryset(self):
           """Return posts from followed users."""
           user = self.request.user
           following = user.following.all()
           return Post.objects.filter(
               author__in=following
           ).select_related('author').prefetch_related('likes')
   ```

3. **Form Validation**
   ```python
   from django import forms
   from django.contrib.auth.forms import UserCreationForm
   from .models import CustomUser
   
   class GreenUniversityRegistrationForm(UserCreationForm):
       """Registration form with Green University validation."""
       
       email = forms.EmailField(required=True)
       student_id = forms.CharField(max_length=9, min_length=9)
       
       class Meta:
           model = CustomUser
           fields = ('username', 'email', 'student_id', 'department', 'batch')
       
       def clean_email(self):
           """Validate Green University email format."""
           email = self.cleaned_data.get('email')
           if not email.endswith('@student.green.edu.bd'):
               raise forms.ValidationError(
                   "Please use your Green University email address."
               )
           return email
   ```

### HTML/CSS Standards

1. **Template Structure**
   ```html
   {% extends 'base.html' %}
   {% load static %}
   
   {% block title %}Social Feed - GreenLink{% endblock %}
   
   {% block extra_css %}
   <link rel="stylesheet" href="{% static 'css/social.css' %}">
   {% endblock %}
   
   {% block content %}
   <div class="container mt-4">
       <div class="row">
           <div class="col-md-8">
               <!-- Main content -->
           </div>
           <div class="col-md-4">
               <!-- Sidebar -->
           </div>
       </div>
   </div>
   {% endblock %}
   
   {% block extra_js %}
   <script src="{% static 'js/social.js' %}"></script>
   {% endblock %}
   ```

2. **CSS Organization**
   ```css
   /* Component-specific styles */
   .post-card {
       background: white;
       border-radius: 8px;
       box-shadow: 0 2px 4px rgba(0,0,0,0.1);
       margin-bottom: 1rem;
       padding: 1rem;
   }
   
   /* Responsive design */
   @media (max-width: 768px) {
       .post-card {
           margin: 0 -15px 1rem -15px;
           border-radius: 0;
       }
   }
   
   /* Green University theme variables */
   :root {
       --green-primary: #8BC4A7;
       --green-secondary: #A8D5BA;
   }
   ```

## 🧪 Testing Guidelines

### Unit Testing
```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostModelTest(TestCase):
    """Test cases for Post model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='123456789@student.green.edu.bd',
            password='testpass123',
            student_id='123456789'
        )
    
    def test_post_creation(self):
        """Test post creation."""
        post = Post.objects.create(
            author=self.user,
            content="Test post content"
        )
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content, "Test post content")
        self.assertTrue(post.created_at)
    
    def test_post_string_representation(self):
        """Test post __str__ method."""
        post = Post.objects.create(
            author=self.user,
            content="This is a test post for string representation"
        )
        expected = f"{self.user.username} - This is a test post for string repr"
        self.assertEqual(str(post), expected)
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage html
```

## 🔧 Database Management

### Migration Workflow
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name 0001
```

### Custom Management Commands
Create custom commands in `management/commands/`:

```python
# accounts/management/commands/create_test_users.py
from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Create test users for development'
    
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10)
    
    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            user = CustomUser.objects.create_user(
                username=f'testuser{i}',
                email=f'12345678{i}@student.green.edu.bd',
                password='testpass123',
                student_id=f'12345678{i}'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {user.username}')
            )
```

## 🚀 Deployment Guide

### Production Settings
```python
# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "green_university_campus.wsgi:application"]
```

## 🔍 Debugging Tips

### Django Debug Toolbar
```python
# Install
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Configure
INTERNAL_IPS = ['127.0.0.1']
```

### Logging Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'greenlink.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🤝 Contributing Guidelines

### Git Workflow

1. **Feature Branch Flow**
   ```bash
   # Create feature branch
   git checkout -b feature/new-chat-system
   
   # Make changes and commit
   git add .
   git commit -m "Add real-time chat functionality"
   
   # Push branch
   git push origin feature/new-chat-system
   
   # Create pull request
   ```

2. **Commit Message Format**
   ```
   feat: add real-time chat system
   fix: resolve profile picture upload issue
   docs: update API documentation
   test: add unit tests for social feed
   refactor: improve database query performance
   ```

### Pull Request Process

1. **Before Submitting**
   - Run tests: `python manage.py test`
   - Check code style: `flake8`
   - Update documentation if needed
   - Test manually on different screen sizes

2. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Manual testing completed
   - [ ] Cross-browser testing done
   
   ## Screenshots (if applicable)
   ```

### Code Review Checklist

- [ ] Code follows Django best practices
- [ ] No hardcoded values (use settings/environment variables)
- [ ] Proper error handling implemented
- [ ] Security considerations addressed
- [ ] Performance impact considered
- [ ] Documentation updated
- [ ] Tests included

## 🛡️ Security Best Practices

### Input Validation
```python
from django.core.exceptions import ValidationError
import re

def validate_student_id(value):
    """Validate student ID format."""
    if not re.match(r'^\d{9}$', value):
        raise ValidationError('Student ID must be exactly 9 digits.')
```

### SQL Injection Prevention
```python
# Good - Using Django ORM
users = CustomUser.objects.filter(department=department)

# Bad - Raw SQL without parameterization
# users = CustomUser.objects.raw(f"SELECT * FROM users WHERE department = '{department}'")

# Good - Parameterized raw SQL (if needed)
users = CustomUser.objects.raw(
    "SELECT * FROM users WHERE department = %s", 
    [department]
)
```

### XSS Prevention
```html
<!-- Templates automatically escape by default -->
{{ user.bio }}  <!-- Safe -->

<!-- For HTML content, use |safe carefully -->
{{ post.content|linebreaks }}  <!-- Safe for line breaks -->

<!-- Never use |safe with user input -->
<!-- {{ user_input|safe }}  DANGEROUS -->
```

## 📈 Performance Optimization

### Database Optimization
```python
# Use select_related for foreign keys
posts = Post.objects.select_related('author').all()

# Use prefetch_related for many-to-many
posts = Post.objects.prefetch_related('likes').all()

# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['author', '-created_at']),
        models.Index(fields=['department']),
    ]
```

### Caching Strategy
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def public_event_list(request):
    return render(request, 'events/public_list.html')

# Manual caching
def get_user_stats(user_id):
    cache_key = f'user_stats_{user_id}'
    stats = cache.get(cache_key)
    if stats is None:
        stats = calculate_user_stats(user_id)
        cache.set(cache_key, stats, 60 * 30)  # 30 minutes
    return stats
```

## 🔧 VS Code Configuration

### Recommended Extensions
- Python
- Django
- Prettier - Code formatter
- GitLens
- Thunder Client (for API testing)

### Workspace Settings
```json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "editor.formatOnSave": true,
    "files.associations": {
        "*.html": "html"
    }
}
```

---

This development guide provides everything you need to start contributing to GreenLink. For questions or clarifications, please refer to the existing code examples or create an issue in the repository.
