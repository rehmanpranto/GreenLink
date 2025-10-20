# GreenLink API Documentation

## 🌐 API Overview

GreenLink provides a comprehensive set of Django views and endpoints for managing the campus social platform. This document outlines all available endpoints, their functionality, and usage patterns.

## 🔐 Authentication Endpoints

### User Registration
**Endpoint**: `/accounts/register/`  
**Method**: `GET`, `POST`  
**Description**: User registration with Green University email validation

**POST Parameters**:
```json
{
  "username": "string",
  "email": "123456789@student.green.edu.bd",
  "password1": "string",
  "password2": "string",
  "student_id": "123456789",
  "department": "Computer Science and Engineering",
  "batch": "2024",
  "first_name": "string",
  "last_name": "string"
}
```

**Validation Rules**:
- Email must match pattern: `\d{9}@student\.green\.edu\.bd`
- Student ID must be exactly 9 digits
- Student ID must be unique
- Password confirmation must match

**Response**:
- Success: Redirect to profile completion
- Error: Form with validation errors

### User Login
**Endpoint**: `/accounts/login/`  
**Method**: `GET`, `POST`  
**Description**: User authentication

**POST Parameters**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response**:
- Success: Redirect to dashboard
- Error: Login form with error message

### User Logout
**Endpoint**: `/accounts/logout/`  
**Method**: `POST`  
**Description**: User session termination

**Response**: Redirect to landing page

### Password Reset
**Endpoint**: `/accounts/password-reset/`  
**Method**: `GET`, `POST`  
**Description**: Password reset request

**POST Parameters**:
```json
{
  "email": "123456789@student.green.edu.bd"
}
```

### Password Reset Confirm
**Endpoint**: `/accounts/password-reset-confirm/<uidb64>/<token>/`  
**Method**: `GET`, `POST`  
**Description**: Password reset confirmation

## 👤 Profile Endpoints

### Profile View
**Endpoint**: `/profile/`  
**Method**: `GET`  
**Description**: View current user's profile
**Authentication**: Required

**Response Data**:
```json
{
  "user": {
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "student_id": "string",
    "department": "string",
    "batch": "string",
    "bio": "string",
    "profile_picture": "url"
  },
  "stats": {
    "posts_count": "integer",
    "followers_count": "integer",
    "following_count": "integer"
  }
}
```

### Profile Edit
**Endpoint**: `/profile/edit/`  
**Method**: `GET`, `POST`  
**Description**: Edit user profile
**Authentication**: Required

**POST Parameters**:
```json
{
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "phone_number": "string",
  "profile_picture": "file"
}
```

### User Profile View
**Endpoint**: `/profile/user/<str:username>/`  
**Method**: `GET`  
**Description**: View another user's profile
**Authentication**: Required

### Follow/Unfollow User
**Endpoint**: `/profile/follow/<str:username>/`  
**Method**: `POST`  
**Description**: Toggle follow status for a user
**Authentication**: Required

**Response**:
```json
{
  "action": "followed|unfollowed",
  "followers_count": "integer"
}
```

## 📱 Social Endpoints

### Social Feed
**Endpoint**: `/social/`  
**Method**: `GET`  
**Description**: Display social feed with posts from followed users
**Authentication**: Required

**Query Parameters**:
- `page`: Page number for pagination

**Response**: Paginated list of posts

### Create Post
**Endpoint**: `/social/create-post/`  
**Method**: `GET`, `POST`  
**Description**: Create a new social post
**Authentication**: Required

**POST Parameters**:
```json
{
  "content": "string (max 2200 characters)",
  "image": "file (optional)"
}
```

### Post Detail
**Endpoint**: `/social/post/<int:post_id>/`  
**Method**: `GET`  
**Description**: View individual post with comments
**Authentication**: Required

### Like/Unlike Post
**Endpoint**: `/social/post/<int:post_id>/like/`  
**Method**: `POST`  
**Description**: Toggle like status for a post
**Authentication**: Required

**Response**:
```json
{
  "action": "liked|unliked",
  "likes_count": "integer"
}
```

### Add Comment
**Endpoint**: `/social/post/<int:post_id>/comment/`  
**Method**: `POST`  
**Description**: Add comment to a post
**Authentication**: Required

**POST Parameters**:
```json
{
  "content": "string"
}
```

### Delete Post
**Endpoint**: `/social/post/<int:post_id>/delete/`  
**Method**: `POST`  
**Description**: Delete own post
**Authentication**: Required
**Authorization**: Post author only

## 💬 Chat Endpoints

### Chat List
**Endpoint**: `/chat/`  
**Method**: `GET`  
**Description**: List all conversations
**Authentication**: Required

### Conversation View
**Endpoint**: `/chat/<int:user_id>/`  
**Method**: `GET`, `POST`  
**Description**: View conversation with specific user
**Authentication**: Required

**POST Parameters**:
```json
{
  "message": "string"
}
```

### Start Conversation
**Endpoint**: `/chat/start/<str:username>/`  
**Method**: `GET`  
**Description**: Start new conversation with user
**Authentication**: Required

## 🎉 Event Endpoints

### Event List
**Endpoint**: `/events/`  
**Method**: `GET`  
**Description**: List all upcoming events

**Query Parameters**:
- `category`: Filter by event category
- `date`: Filter by date

### Event Detail
**Endpoint**: `/events/<int:event_id>/`  
**Method**: `GET`  
**Description**: View event details

### Create Event
**Endpoint**: `/events/create/`  
**Method**: `GET`, `POST`  
**Description**: Create new event
**Authentication**: Required

**POST Parameters**:
```json
{
  "title": "string",
  "description": "string",
  "date": "datetime",
  "location": "string",
  "category": "string",
  "image": "file (optional)"
}
```

### RSVP Event
**Endpoint**: `/events/<int:event_id>/rsvp/`  
**Method**: `POST`  
**Description**: RSVP to event
**Authentication**: Required

**Response**:
```json
{
  "action": "attending|not_attending",
  "attendees_count": "integer"
}
```

## 🏠 Home Endpoints

### Landing Page
**Endpoint**: `/`  
**Method**: `GET`  
**Description**: Public landing page with university information

### Dashboard
**Endpoint**: `/dashboard/`  
**Method**: `GET`  
**Description**: Student dashboard with quick stats
**Authentication**: Required

**Response Data**:
```json
{
  "stats": {
    "total_students": "integer",
    "active_events": "integer",
    "departments": "integer",
    "posts_today": "integer"
  },
  "recent_posts": "array",
  "upcoming_events": "array"
}
```

## 🔍 Search Endpoints

### General Search
**Endpoint**: `/search/`  
**Method**: `GET`  
**Description**: Search across users, posts, and events

**Query Parameters**:
- `q`: Search query
- `type`: Search type (users, posts, events, all)

### User Search
**Endpoint**: `/search/users/`  
**Method**: `GET`  
**Description**: Search for users
**Authentication**: Required

**Query Parameters**:
- `q`: Search query
- `department`: Filter by department
- `batch`: Filter by batch

## 📊 API Response Patterns

### Success Response Format
```json
{
  "status": "success",
  "data": {},
  "message": "Operation completed successfully"
}
```

### Error Response Format
```json
{
  "status": "error",
  "errors": {
    "field_name": ["Error message"]
  },
  "message": "Operation failed"
}
```

### Pagination Format
```json
{
  "count": "integer",
  "next": "url|null",
  "previous": "url|null",
  "results": []
}
```

## 🛡️ Authentication & Permissions

### Authentication Requirements
- Most endpoints require user authentication
- Public endpoints: Landing page, event list (read-only)
- Authentication via Django sessions

### Permission Levels
- **Public**: No authentication required
- **Authenticated**: Valid user session required
- **Owner**: User can only access/modify their own content
- **Admin**: Staff/superuser access required

### Security Headers
All API responses include appropriate security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

## 📝 Request/Response Examples

### Register New User
```bash
POST /accounts/register/
Content-Type: application/x-www-form-urlencoded

username=john_doe&email=123456789@student.green.edu.bd&password1=SecurePass123&password2=SecurePass123&student_id=123456789&department=Computer Science and Engineering&batch=2024&first_name=John&last_name=Doe
```

### Create Social Post
```bash
POST /social/create-post/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=...

content=Just finished my final project! Excited to graduate. #graduation #cse #greenuniversity
```

### Like a Post
```bash
POST /social/post/123/like/
Cookie: sessionid=...

Response:
{
  "action": "liked",
  "likes_count": 15
}
```

## 🚨 Error Handling

### Common HTTP Status Codes
- `200 OK`: Successful request
- `302 Found`: Redirect (common for form submissions)
- `400 Bad Request`: Invalid form data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Validation Errors
Form validation errors are displayed in templates with appropriate styling and user-friendly messages.

## 🔄 Rate Limiting

Currently, no rate limiting is implemented, but for production deployment, consider:
- Login attempt limiting
- Post creation rate limiting
- API request throttling

## 📱 Mobile Considerations

All endpoints are designed to work with:
- Responsive web interface
- Mobile browsers
- Future mobile app integration
- Progressive Web App (PWA) compatibility

---

This API documentation provides comprehensive coverage of GreenLink's functionality and serves as a reference for developers working with the platform.
