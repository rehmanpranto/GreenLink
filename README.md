# GreenLink - Campus Social Network

A modern, Facebook-style social networking platform designed specifically for university campuses, built with Django and featuring real-time interactions, multimedia sharing, and comprehensive campus life management.

## 🌟 Overview

GreenLink transforms the traditional campus experience by providing students with a comprehensive social platform that combines the best features of Facebook, Twitter, and LinkedIn, all tailored specifically for university life.

## 🏗️ Project Structure - Campus Social Network

# GreenLink - Campus Social Network

A modern, Facebook-style social networking platform designed specifically for university campuses, built with Django and featuring real-time interactions, multimedia sharing, and comprehensive campus life management.

## � Overview

GreenLink transforms the traditional campus experience by providing students with a comprehensive social platform that combines the best features of Facebook, Twitter, and LinkedIn, all tailored specifically for university life.

## �🏗️ Project Structure

```
campuslink-working/
├── 📁 accounts/           # User authentication & management
├── 📁 chat/              # Real-time messaging system
├── 📁 events/            # Campus events & activities
├── 📁 green_university_campus/  # Main Django project settings
├── 📁 home/              # Landing pages & public content
├── 📁 profiles/          # User profiles & dashboards
├── 📁 social/            # Core social networking features
├── 📁 static/            # CSS, JavaScript, images
├── 📁 templates/         # HTML templates
├── 📁 docs/              # Project documentation
├── 📄 manage.py          # Django management script
├── 📄 run_webapp.py      # One-click setup and run script
├── 📄 start_greenlink.bat # Windows batch file launcher
├── 📄 start_greenlink.sh # Linux/Mac shell script launcher
├── 📄 requirements.txt   # Development dependencies
├── 📄 requirements-production.txt  # Production dependencies
├── 📄 Procfile           # Deployment configuration
├── 📄 runtime.txt        # Python version specification
└── 📄 db.sqlite3         # Local development database
```

## ✨ Key Features

### 🎭 Facebook-Style Interface
- **Modern Three-Column Layout**: Stories, main feed, and sidebar navigation
- **Real-Time Reactions**: Like, Love, Laugh, Wow, Sad, Angry with emoji support
- **Interactive Comments**: AJAX-powered comment system with instant updates
- **Post Composer**: Rich text editor with image upload support
- **Stories Feature**: Create and view temporary story content

### 📱 Social Networking
- **User Profiles**: Comprehensive profile management with photos and info
- **Friend System**: Send/accept friend requests and manage connections
- **Groups**: Join and create study groups and interest communities
- **News Feed**: Personalized content feed with engagement metrics
- **Notifications**: Real-time updates for interactions and activities

### 🎓 Campus-Specific Features
- **Academic Integration**: Department, batch, and course information
- **Event Management**: Campus events, workshops, and activities
- **Study Groups**: Academic collaboration and study sessions
- **Marketplace**: Buy/sell textbooks and campus resources
- **Student Authentication**: Green University email validation system

### 🛠️ Technical Features
- **Responsive Design**: Mobile-first approach with adaptive layouts
- **AJAX Interactions**: Seamless user experience without page reloads
- **Image Handling**: Secure file uploads with validation
- **Authentication**: Complete user registration and login system
- **Database Optimization**: Efficient queries with proper relationships

## 🚀 Quick Start

### 🌟 **One-Click Setup (Recommended)**

Choose your preferred method to run GreenLink:

#### Option 1: Python Script (All Platforms)
```bash
python run_webapp.py
```

#### Option 2: Windows Batch File
Double-click `start_greenlink.bat` or run:
```cmd
start_greenlink.bat
```

#### Option 3: Linux/Mac Shell Script
```bash
chmod +x start_greenlink.sh
./start_greenlink.sh
```

**All scripts will automatically:**
- ✅ Check Python version compatibility
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up environment configuration
- ✅ Run database migrations
- ✅ Collect static files
- ✅ Offer to create admin user
- ✅ Start the development server
- ✅ Open your browser to the application

### 📋 **Manual Setup**

If you prefer manual setup:

#### Prerequisites
- Python 3.11+
- Django 4.2.7
- Virtual environment support

#### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd campuslink-working
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Development: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

## 📦 Dependencies

### Core Framework
- **Django 4.2.7**: Web framework
- **Pillow 10.0.1**: Image processing
- **Channels 4.0.0**: WebSocket support for real-time features

### UI/UX Libraries
- **django-crispy-forms 2.0**: Beautiful form rendering
- **crispy-bootstrap5 0.7**: Bootstrap 5 integration
- **django-widget-tweaks 1.5.0**: Form widget customization

### Production Dependencies
- **gunicorn 21.2.0**: WSGI HTTP Server
- **whitenoise 6.6.0**: Static file serving
- **python-decouple 3.8**: Environment configuration
- **django-cors-headers 4.3.1**: CORS handling

## 🎨 Design System

### Color Palette
```css
--green-primary: #8BC4A7      /* Primary brand color */
--green-secondary: #A8D5BA    /* Secondary accents */
--green-accent: #6FA88A       /* Interactive elements */
--facebook-blue: #1877F2      /* Facebook-style blue */
--white: #FFFFFF              /* Clean backgrounds */
--light-gray: #F8F9FA         /* Subtle backgrounds */
```

### Typography
- **Primary Font**: Inter (modern, readable)
- **Heading Font**: Poppins (friendly, approachable)
- **Icon Library**: Font Awesome 6.4.0

## 🔧 Configuration

### Environment Variables
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-database-url  # For production
```

### Database Configuration
- **Development**: SQLite3 (included)
- **Production**: PostgreSQL (recommended)

## 📱 App Architecture

### accounts/
- User registration and authentication
- Custom user model with campus-specific fields
- Email verification and password reset

### social/
- Core social networking functionality
- Posts, comments, reactions, and sharing
- Friend requests and connections
- Facebook-style feed with AJAX interactions

### profiles/
- User profile management
- Dashboard with activity overview
- Privacy settings and preferences

### chat/
- Real-time messaging system
- WebSocket support for instant communication
- Group chats and direct messages

### events/
- Campus event management
- Event creation, registration, and notifications
- Calendar integration

### home/
- Landing pages for anonymous users
- Public information and onboarding

## 🎯 Usage Examples

### Creating a Post
```javascript
// AJAX post creation with image upload
function createPost(content, images) {
    const formData = new FormData();
    formData.append('content', content);
    images.forEach(image => formData.append('images', image));
    
    fetch('/social/post/create/', {
        method: 'POST',
        body: formData,
        headers: {'X-CSRFToken': getCookie('csrftoken')}
    }).then(response => response.json())
      .then(data => updateFeed(data));
}
```

### Reacting to Posts
```javascript
// Facebook-style reactions
function reactToPost(postId, reactionType) {
    fetch(`/social/react/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({reaction: reactionType})
    }).then(response => response.json())
      .then(data => updateReactionDisplay(data));
}
```

## 🚀 Deployment

### Production Setup
1. **Set environment variables**
   ```bash
   export SECRET_KEY="your-production-secret-key"
   export DEBUG=False
   export DATABASE_URL="postgresql://..."
   ```

2. **Install production dependencies**
   ```bash
   pip install -r requirements-production.txt
   ```

3. **Configure static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

### Deployment Platforms
- **Heroku**: Ready with Procfile
- **Railway**: Database and static file configuration included
- **DigitalOcean**: App Platform compatible
- **AWS/GCP**: Container deployment ready

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:
- [API Reference](docs/API.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Database Schema](docs/DATABASE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Development Setup](docs/DEVELOPMENT.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎓 Campus Integration

GreenLink is designed specifically for university environments with features like:
- Department and batch organization
- Academic calendar integration
- Study group formation
- Campus event management
- Resource sharing marketplace
- Student life enhancement

---

**Built with ❤️ for the modern campus community**
```
