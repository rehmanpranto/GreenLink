# GreenLink Architecture Documentation

## 🏗️ System Architecture Overview

GreenLink is built using Django's Model-View-Template (MVT) architecture pattern, providing a robust and scalable foundation for the campus social platform.

## 📊 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│                 │    │                 │    │                 │
│ - Bootstrap 5   │◄──►│ - Django 4.2.7  │◄──►│ - SQLite        │
│ - JavaScript    │    │ - Python 3.13   │    │ - File Storage  │
│ - CSS Custom    │    │ - Authentication │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🏛️ Django Project Structure

### Core Project (`green_university_campus/`)
- **settings.py**: Application configuration and environment settings
- **urls.py**: Main URL routing configuration
- **wsgi.py**: WSGI application for deployment
- **asgi.py**: ASGI application for async features (future WebSocket support)

### Application Architecture

GreenLink follows Django's app-based architecture with 6 specialized apps:

```
green_university_campus/
├── accounts/          # Authentication & User Management
├── profiles/          # Student Profile Management
├── social/           # Social Networking Features
├── chat/             # Messaging System
├── events/           # Event Management
└── home/             # Landing Pages & Dashboard
```

## 📱 Application Layer Details

### 1. Accounts App (`accounts/`)
**Purpose**: Handle user authentication, registration, and account management

**Key Components**:
- `CustomUser` model extending Django's AbstractUser
- Green University email validation system
- Student ID verification (9-digit format)
- Department and batch tracking
- Profile picture management

**Models**:
```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=9, unique=True)
    department = models.CharField(max_length=100)
    batch = models.CharField(max_length=10)
    profile_picture = models.ImageField()
    bio = models.TextField()
    phone_number = models.CharField(max_length=15)
```

**Views**:
- User registration with validation
- Login/logout functionality
- Profile completion workflow
- Password reset system

### 2. Profiles App (`profiles/`)
**Purpose**: Manage detailed student profiles and social connections

**Key Features**:
- Extended profile information
- Academic background tracking
- Social connections (following/followers)
- Profile visibility controls

**Models**:
- `Profile` (One-to-One with CustomUser)
- `Connection` (Many-to-Many relationships)
- `AcademicBackground`
- `Experience`

### 3. Social App (`social/`)
**Purpose**: Core social networking functionality

**Key Features**:
- Post creation and sharing
- News feed generation
- Like/comment system
- Hashtag support
- Content moderation

**Models**:
```python
class Post(models.Model):
    author = models.ForeignKey(CustomUser)
    content = models.TextField(max_length=2200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts')
    hashtags = models.ManyToManyField(Hashtag)
```

### 4. Chat App (`chat/`)
**Purpose**: Real-time messaging system

**Key Features**:
- Direct messaging between students
- Message history
- Online status tracking
- Future: Group chat support

**Models**:
- `Conversation`
- `Message`
- `MessageStatus`

### 5. Events App (`events/`)
**Purpose**: Campus event management and discovery

**Key Features**:
- Event creation and management
- RSVP system
- Event categories
- Calendar integration

**Models**:
- `Event`
- `EventCategory`
- `EventAttendance`

### 6. Home App (`home/`)
**Purpose**: Landing pages and dashboard

**Key Features**:
- Beautiful landing page with Green University branding
- Student dashboard
- Quick navigation
- Campus statistics

## 🎨 Frontend Architecture

### Template Structure
```
templates/
├── base.html                 # Base template with common elements
├── components/               # Reusable template components
│   ├── navbar.html
│   ├── footer.html
│   └── sidebar.html
├── accounts/                 # Authentication templates
├── profiles/                 # Profile templates
├── social/                   # Social feed templates
├── chat/                     # Messaging templates
├── events/                   # Event templates
└── home/                     # Landing and dashboard templates
```

### CSS Architecture
- **Bootstrap 5**: Primary CSS framework
- **Custom CSS**: Green University themed components
- **Responsive Design**: Mobile-first approach
- **CSS Variables**: Consistent color scheme

```css
/* Green University Design System */
:root {
  --green-primary: #8BC4A7;
  --green-secondary: #A8D5BA;
  --green-accent: #6FA88A;
  --green-light: #C8E6D0;
  --green-dark: #4A8068;
}
```

## 🗄️ Database Architecture

### Database Design Principles
- **Normalized Structure**: Efficient data organization
- **Referential Integrity**: Proper foreign key relationships
- **Scalability**: Design supports growth
- **Performance**: Indexed fields for common queries

### Key Relationships
```
CustomUser (1) ←→ (1) Profile
CustomUser (1) ←→ (M) Post
CustomUser (M) ←→ (M) CustomUser (followers/following)
Post (1) ←→ (M) Comment
Post (M) ←→ (M) CustomUser (likes)
Event (1) ←→ (M) EventAttendance
```

## 🔐 Security Architecture

### Authentication & Authorization
- **Django Authentication**: Built-in user authentication system
- **Custom User Model**: Extended with university-specific fields
- **Email Validation**: Green University domain validation
- **CSRF Protection**: Cross-Site Request Forgery protection
- **Password Security**: Django's built-in password hashing

### Data Protection
- **Input Validation**: Server-side form validation
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping
- **Secure Headers**: Security middleware configuration

## 📡 URL Routing Architecture

### Main URL Configuration (`green_university_campus/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('profile/', include('profiles.urls')),
    path('social/', include('social.urls')),
    path('chat/', include('chat.urls')),
    path('events/', include('events.urls')),
]
```

### App-Level URL Patterns
Each app maintains its own URL configuration for modular organization.

## 🚀 Deployment Architecture

### Development Environment
- **SQLite Database**: Lightweight for development
- **Django Development Server**: Built-in server
- **Debug Mode**: Detailed error reporting

### Production Considerations
- **PostgreSQL**: Recommended production database
- **Gunicorn**: WSGI HTTP server
- **Nginx**: Reverse proxy and static file serving
- **Redis**: Caching and session storage
- **Celery**: Background task processing

## 📈 Performance Considerations

### Database Optimization
- **Query Optimization**: Use of select_related and prefetch_related
- **Database Indexing**: Proper indexing on frequently queried fields
- **Connection Pooling**: Efficient database connections

### Caching Strategy
- **Template Caching**: Cache rendered templates
- **Database Caching**: Cache frequent database queries
- **Static File Caching**: Browser caching for static assets

### Frontend Performance
- **Minified Assets**: Compressed CSS and JavaScript
- **Image Optimization**: Proper image formats and sizes
- **Lazy Loading**: Load content as needed

## 🔄 Data Flow Architecture

### Request/Response Cycle
1. **URL Routing**: Django URL dispatcher
2. **View Processing**: Business logic execution
3. **Model Interaction**: Database operations
4. **Template Rendering**: HTML generation
5. **Response Delivery**: HTTP response to client

### Authentication Flow
1. **Login Request**: User credentials submission
2. **Validation**: Email format and credentials verification
3. **Session Creation**: Django session management
4. **Authorization**: Permission checking for protected views

## 🧪 Testing Architecture

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **Functional Tests**: End-to-end user journey testing
- **Security Tests**: Authentication and authorization testing

### Test Organization
```
tests/
├── test_models.py        # Model testing
├── test_views.py         # View testing
├── test_forms.py         # Form validation testing
└── test_integration.py   # Integration testing
```

## 📊 Monitoring & Logging

### Logging Strategy
- **Application Logs**: Django application logging
- **Database Logs**: Query performance monitoring
- **Security Logs**: Authentication and authorization events
- **Error Tracking**: Comprehensive error reporting

### Performance Monitoring
- **Response Time Tracking**: View performance monitoring
- **Database Query Monitoring**: SQL query optimization
- **Memory Usage**: Application resource monitoring

---

This architecture provides a solid foundation for GreenLink's growth and ensures maintainability, scalability, and security for the Green University student community.
