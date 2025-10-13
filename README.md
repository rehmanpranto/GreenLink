# GreenLink

**Green Unive### Key Features
- 🔐 **Secure Authentication**: Custom user model with Green University email validation
- 👥 **Student Verification**: 9-digit student ID validation system
- 💬 **Re## 🌟 Features Overviewl-time Chat**: Messaging system for student communication
- 📅 **Event Management**: Create and discover campus events and activities
- 🎨 **Sage Green Theme**: Beautiful sage green color scheme (#8BC4A7) reflecting nature
- 📱 **Mobile Responsive**: Bootstrap-based responsive designonnection Platform**

A modern, secure, and user-friendly campus social platform for Green University of Bangladesh students. Built with Django, Bootstrap, and modern web technologies to connect students across campus.

## 🚀 Features

### 🐦 Twitter-like Social Features
- **News Feed**: Real-time social feed with posts from followed classmates
- **Post Types**: Regular posts, project showcases, achievements, job updates, academic news
- **Engagement**: Like, comment, share, and bookmark posts
- **Hashtags**: Trending topics and hashtag discovery
- **Following System**: Follow/unfollow classmates with follower counts
- **Character Limit**: Twitter-style 2200 character limit with live counter
- **Media Sharing**: Photo and document attachments

### 💼 LinkedIn-like Professional Features
- **Professional Profiles**: Detailed academic and professional profiles
- **Experience Section**: Internships, jobs, volunteer work, projects
- **Education History**: Academic background and achievements
- **Skills & Endorsements**: Skill listings with peer endorsements
- **Professional Connections**: Send and manage connection requests
- **Study Groups**: Academic collaboration and group formation
- **Career Updates**: Job postings and career milestone sharing

### 🎓 University-Specific Features
- **Student Authentication**: Secure login with Green University email validation
- **Department Integration**: Department-wise networking and content filtering
- **Batch Connections**: Connect with classmates from same admission batch
- **Academic Calendar**: Campus events and academic deadlines
- **GPA Tracking**: Academic performance sharing (optional)
- **Course Integration**: Course-specific study groups and discussions

### 🔔 Engagement & Notifications
- **Real-time Notifications**: Instant alerts for likes, comments, follows, connections
- **Smart Suggestions**: AI-powered classmate and connection recommendations
- **Trending Content**: Popular hashtags and topics within university
- **Activity Feed**: Comprehensive activity tracking and analytics

## 📱 Pages & Features

### Core Pages
- **Dashboard (/)**: Personalized student dashboard with quick stats and navigation
- **Profile (/profile)**: Detailed student profiles with academic information
- **Social Feed (/social)**: Campus-wide social networking and post sharing
- **Messages (/chat)**: Real-time messaging system for student communication
- **Events (/events)**: Campus event discovery and creation platform
- **Authentication**: Secure login/registration with Green University email validation

### Key Features
- 🔐 **Secure Authentication**: Custom user model with Green University email validation
- � **Student Verification**: 9-digit student ID validation system
- � **Real-time Chat**: Messaging system for student communication
- � **Event Management**: Create and discover campus events and activities
- � **Green Theme**: Forest green color scheme reflecting university branding
- 📱 **Mobile Responsive**: Bootstrap-based responsive design

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7** - Python web framework
- **SQLite** - Database for development
- **Pillow** - Image processing for profile pictures
- **Django Crispy Forms** - Enhanced form rendering

### Frontend
- **Bootstrap 5** - CSS framework for responsive design
- **Font Awesome** - Icon library
- **JavaScript** - Client-side interactivity

### Dependencies
- **django-crispy-forms** - Enhanced form rendering
- **crispy-bootstrap5** - Bootstrap 5 integration for forms
- **django-widget-tweaks** - Template form field customization

## 📁 Project Structure

```
greenlink/
├── green_university_campus/       # Main Django project
│   ├── settings.py                # Project settings
│   ├── urls.py                    # URL routing
│   └── wsgi.py                    # WSGI configuration
├── accounts/                      # Authentication app
│   ├── models.py                 # Custom user model
│   ├── views.py                  # Authentication views
│   ├── forms.py                  # Login/registration forms
│   └── urls.py                   # Auth URL patterns
├── profiles/                     # Student profiles app
│   ├── models.py                # Profile models
│   ├── views.py                 # Profile views
│   └── urls.py                  # Profile URL patterns
├── social/                      # Social networking app
│   ├── models.py               # Post/feed models
│   ├── views.py                # Social views
│   └── urls.py                 # Social URL patterns
├── chat/                       # Messaging app
│   ├── models.py              # Message models
│   ├── views.py               # Chat views
│   └── urls.py                # Chat URL patterns
├── events/                     # Events app
│   ├── models.py              # Event models
│   ├── views.py               # Event views
│   └── urls.py                # Event URL patterns
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── accounts/              # Authentication templates
│   ├── profiles/              # Profile templates
│   ├── social/                # Social templates
│   ├── chat/                  # Chat templates
│   └── events/                # Event templates
├── static/                     # Static files
│   └── css/                   # Custom CSS
├── manage.py                   # Django management script
└── requirements.txt            # Python dependencies
```

## 🎨 Design System

### Green University Theme
The application uses Green University's branding colors defined in `static/css/green_university.css`:

```css
/* Green University Colors */
--green-primary: #8BC4A7;    /* Sage Green */
--green-secondary: #A8D5BA;  /* Light Sage */
--green-accent: #6FA88A;     /* Darker Sage */
--green-light: #C8E6D0;      /* Very Light Sage */
--green-dark: #4A8068;       /* Dark Sage */
```

### UI Components
- Bootstrap 5 responsive grid system
- Custom green-themed components
- Font Awesome icons
- Crispy forms for enhanced form rendering

### Authentication System
- Custom user model with Green University validation
- Email format: `123456789@student.green.edu.bd`
- 9-digit student ID validation
- Department and batch tracking
- Profile picture support

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository** (or use the existing directory)
   ```bash
   cd campuslink-working
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   Navigate to `http://127.0.0.1:8000`

### Available Django Commands

- `python manage.py runserver` - Start development server
- `python manage.py makemigrations` - Create database migrations
- `python manage.py migrate` - Apply database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files for production

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root for sensitive settings:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Django Settings
Key settings in `green_university_campus/settings.py`:
- Custom user model: `accounts.CustomUser`
- Green University specific configurations
- Bootstrap 5 and Font Awesome integration
- Media and static files handling

### User Registration Requirements
- Valid Green University email format: `123456789@student.green.edu.bd`
- 9-digit student ID (must be unique)
- Department and batch information
- Email verification system ready for implementation

## � Features Overview

### Authentication System
- Secure registration with Green University email validation
- 9-digit student ID verification system
- Department and batch information tracking
- Profile picture upload support

### Social Features
- Campus-wide social feed for sharing posts
- Student profile discovery and connections
- Real-time messaging system
- Event creation and discovery platform

### User Experience
- Mobile-responsive Bootstrap design
- Beautiful sage green themed interface (#8BC4A7)
- Intuitive navigation and user flows
- Admin panel for platform management

## 🔮 Future Enhancements

### Planned Features
- Real-time chat with WebSocket integration
- Advanced search and filtering
- File sharing in messages
- Event RSVP and notifications
- Study group formation tools
- Academic calendar integration

### Technical Improvements
- PostgreSQL database for production
- Redis caching for better performance
- Celery for background tasks
- Email notification system
- API endpoints for mobile app integration

## 📄 License

This project is built for educational purposes for Green University of Bangladesh students.

## 🤝 Contributing

When extending this project:
1. Follow Django best practices and PEP 8 style guide
2. Maintain Green University branding consistency
3. Add proper error handling and validation
4. Include appropriate documentation
5. Write tests for new features

## 📞 Support

For technical questions or feature requests, please refer to the project documentation or contact the development team.

---

**Built with 💚 for Green University Students**
      // other options...
    },
  },
])
```
