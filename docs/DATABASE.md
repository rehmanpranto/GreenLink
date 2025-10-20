# GreenLink Database Documentation

## 🗄️ Database Schema Overview

GreenLink uses a relational database design optimized for social networking features while maintaining academic institution requirements. The database supports user authentication, social interactions, messaging, events, and profile management.

## 📊 Database Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CustomUser    │◄──►│    Profile      │    │      Post       │
│                 │    │                 │    │                 │
│ - id (PK)       │    │ - id (PK)       │    │ - id (PK)       │
│ - username      │    │ - user_id (FK)  │    │ - author_id (FK)│
│ - email         │    │ - bio           │    │ - content       │
│ - student_id    │    │ - phone         │    │ - created_at    │
│ - department    │    │ - created_at    │    │ - likes (M2M)   │
│ - batch         │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              │
         │                                              │
         ▼                                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Following     │    │    Message      │    │    Comment      │
│                 │    │                 │    │                 │
│ - follower (FK) │    │ - id (PK)       │    │ - id (PK)       │
│ - following(FK) │    │ - sender_id(FK) │    │ - post_id (FK)  │
│ - created_at    │    │ - receiver(FK)  │    │ - author_id(FK) │
│                 │    │ - content       │    │ - content       │
└─────────────────┘    │ - timestamp     │    │ - created_at    │
                       │ - is_read       │    │                 │
                       └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Event       │    │ EventAttendance │    │    Hashtag      │
│                 │    │                 │    │                 │
│ - id (PK)       │    │ - id (PK)       │    │ - id (PK)       │
│ - title         │    │ - event_id (FK) │    │ - name          │
│ - description   │    │ - user_id (FK)  │    │ - posts (M2M)   │
│ - date          │    │ - status        │    │ - created_at    │
│ - location      │    │ - rsvp_date     │    │                 │
│ - organizer(FK) │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🏗️ Table Structures

### CustomUser Table
**Purpose**: Extended Django user model with university-specific fields

```sql
CREATE TABLE accounts_customuser (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254) UNIQUE NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP NOT NULL DEFAULT NOW(),
    student_id VARCHAR(9) UNIQUE NOT NULL,
    department VARCHAR(100) NOT NULL,
    batch VARCHAR(10) NOT NULL,
    bio TEXT,
    profile_picture VARCHAR(100),
    phone_number VARCHAR(15),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_customuser_email ON accounts_customuser(email);
CREATE INDEX idx_customuser_student_id ON accounts_customuser(student_id);
CREATE INDEX idx_customuser_department ON accounts_customuser(department);
CREATE INDEX idx_customuser_batch ON accounts_customuser(batch);
```

**Constraints**:
- Email must follow pattern: `^\d{9}@student\.green\.edu\.bd$`
- Student ID must be exactly 9 digits
- Username must be unique
- Email must be unique

### Profile Table
**Purpose**: Extended profile information for users

```sql
CREATE TABLE profiles_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES accounts_customuser(id),
    bio TEXT,
    location VARCHAR(100),
    website VARCHAR(200),
    birth_date DATE,
    phone_number VARCHAR(15),
    linkedin_url VARCHAR(200),
    github_url VARCHAR(200),
    skills TEXT[],
    interests TEXT[],
    gpa DECIMAL(3,2),
    graduation_year INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_profile_user ON profiles_profile(user_id);
CREATE INDEX idx_profile_graduation_year ON profiles_profile(graduation_year);
```

### Following Table
**Purpose**: Many-to-many relationship for user following system

```sql
CREATE TABLE social_following (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    following_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(follower_id, following_id),
    CHECK (follower_id != following_id)
);

-- Indexes
CREATE INDEX idx_following_follower ON social_following(follower_id);
CREATE INDEX idx_following_following ON social_following(following_id);
CREATE INDEX idx_following_created ON social_following(created_at);
```

### Post Table
**Purpose**: Social media posts with content and metadata

```sql
CREATE TABLE social_post (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    content TEXT NOT NULL CHECK (LENGTH(content) <= 2200),
    image VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_pinned BOOLEAN NOT NULL DEFAULT FALSE,
    visibility VARCHAR(20) NOT NULL DEFAULT 'public',
    like_count INTEGER NOT NULL DEFAULT 0,
    comment_count INTEGER NOT NULL DEFAULT 0
);

-- Indexes
CREATE INDEX idx_post_author ON social_post(author_id);
CREATE INDEX idx_post_created ON social_post(created_at DESC);
CREATE INDEX idx_post_visibility ON social_post(visibility);
CREATE INDEX idx_post_author_created ON social_post(author_id, created_at DESC);
```

### Post Likes Table
**Purpose**: Many-to-many relationship for post likes

```sql
CREATE TABLE social_post_likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES social_post(id),
    user_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(post_id, user_id)
);

-- Indexes
CREATE INDEX idx_post_likes_post ON social_post_likes(post_id);
CREATE INDEX idx_post_likes_user ON social_post_likes(user_id);
```

### Comment Table
**Purpose**: Comments on social posts

```sql
CREATE TABLE social_comment (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES social_post(id),
    author_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    parent_id INTEGER REFERENCES social_comment(id),
    content TEXT NOT NULL CHECK (LENGTH(content) <= 500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_edited BOOLEAN NOT NULL DEFAULT FALSE
);

-- Indexes
CREATE INDEX idx_comment_post ON social_comment(post_id);
CREATE INDEX idx_comment_author ON social_comment(author_id);
CREATE INDEX idx_comment_parent ON social_comment(parent_id);
CREATE INDEX idx_comment_created ON social_comment(created_at);
```

### Message Table
**Purpose**: Direct messaging between users

```sql
CREATE TABLE chat_message (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    receiver_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    content TEXT NOT NULL CHECK (LENGTH(content) <= 1000),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    message_type VARCHAR(20) NOT NULL DEFAULT 'text',
    attachment VARCHAR(100)
);

-- Indexes
CREATE INDEX idx_message_sender ON chat_message(sender_id);
CREATE INDEX idx_message_receiver ON chat_message(receiver_id);
CREATE INDEX idx_message_timestamp ON chat_message(timestamp DESC);
CREATE INDEX idx_message_conversation ON chat_message(sender_id, receiver_id, timestamp);
CREATE INDEX idx_message_unread ON chat_message(receiver_id, is_read);
```

### Event Table
**Purpose**: Campus events and activities

```sql
CREATE TABLE events_event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    organizer_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    date_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    location VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    max_attendees INTEGER,
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    image VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_event_organizer ON events_event(organizer_id);
CREATE INDEX idx_event_date ON events_event(date_time);
CREATE INDEX idx_event_category ON events_event(category);
CREATE INDEX idx_event_public ON events_event(is_public);
```

### Event Attendance Table
**Purpose**: Track event RSVPs and attendance

```sql
CREATE TABLE events_eventattendance (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events_event(id),
    user_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    status VARCHAR(20) NOT NULL DEFAULT 'going',
    rsvp_date TIMESTAMP NOT NULL DEFAULT NOW(),
    attended BOOLEAN,
    UNIQUE(event_id, user_id)
);

-- Indexes
CREATE INDEX idx_attendance_event ON events_eventattendance(event_id);
CREATE INDEX idx_attendance_user ON events_eventattendance(user_id);
CREATE INDEX idx_attendance_status ON events_eventattendance(status);
```

### Hashtag Table
**Purpose**: Track hashtags in posts

```sql
CREATE TABLE social_hashtag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE social_post_hashtags (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES social_post(id),
    hashtag_id INTEGER NOT NULL REFERENCES social_hashtag(id),
    UNIQUE(post_id, hashtag_id)
);

-- Indexes
CREATE INDEX idx_hashtag_name ON social_hashtag(name);
CREATE INDEX idx_hashtag_usage ON social_hashtag(usage_count DESC);
```

## 🔍 Database Queries and Performance

### Common Query Patterns

1. **Social Feed Query**
   ```sql
   SELECT p.*, u.username, u.first_name, u.last_name, u.profile_picture,
          COUNT(pl.id) as like_count,
          COUNT(c.id) as comment_count
   FROM social_post p
   JOIN accounts_customuser u ON p.author_id = u.id
   LEFT JOIN social_post_likes pl ON p.id = pl.post_id
   LEFT JOIN social_comment c ON p.id = c.post_id
   WHERE p.author_id IN (
       SELECT following_id FROM social_following WHERE follower_id = ?
   )
   GROUP BY p.id, u.id
   ORDER BY p.created_at DESC
   LIMIT 10 OFFSET ?;
   ```

2. **User Search Query**
   ```sql
   SELECT id, username, first_name, last_name, department, batch, profile_picture
   FROM accounts_customuser
   WHERE (
       LOWER(first_name) LIKE LOWER(?) OR
       LOWER(last_name) LIKE LOWER(?) OR
       LOWER(username) LIKE LOWER(?)
   )
   AND department = COALESCE(?, department)
   AND batch = COALESCE(?, batch)
   ORDER BY username
   LIMIT 20;
   ```

3. **Unread Messages Count**
   ```sql
   SELECT COUNT(*)
   FROM chat_message
   WHERE receiver_id = ? AND is_read = FALSE;
   ```

### Performance Optimization

1. **Database Indexes**
   ```sql
   -- Composite indexes for common queries
   CREATE INDEX idx_post_author_created ON social_post(author_id, created_at DESC);
   CREATE INDEX idx_message_receiver_unread ON chat_message(receiver_id, is_read);
   CREATE INDEX idx_following_follower_created ON social_following(follower_id, created_at DESC);
   ```

2. **Query Optimization**
   ```python
   # Django ORM optimization
   # Bad: N+1 queries
   posts = Post.objects.all()
   for post in posts:
       print(post.author.username)  # Hits database each time
   
   # Good: Single query with join
   posts = Post.objects.select_related('author').all()
   for post in posts:
       print(post.author.username)  # No additional queries
   
   # Good: Prefetch related for M2M
   posts = Post.objects.prefetch_related('likes', 'hashtags').all()
   ```

## 🔐 Database Security

### Access Control
```sql
-- Application user (limited permissions)
CREATE USER greenlink_app WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE greenlink TO greenlink_app;
GRANT USAGE ON SCHEMA public TO greenlink_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO greenlink_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO greenlink_app;

-- Read-only user for analytics
CREATE USER greenlink_readonly WITH PASSWORD 'readonly_password';
GRANT CONNECT ON DATABASE greenlink TO greenlink_readonly;
GRANT USAGE ON SCHEMA public TO greenlink_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO greenlink_readonly;
```

### Data Validation Constraints
```sql
-- Email format validation
ALTER TABLE accounts_customuser ADD CONSTRAINT check_email_format
CHECK (email ~ '^\d{9}@student\.green\.edu\.bd$');

-- Student ID format validation
ALTER TABLE accounts_customuser ADD CONSTRAINT check_student_id_format
CHECK (student_id ~ '^\d{9}$');

-- Post content length
ALTER TABLE social_post ADD CONSTRAINT check_content_length
CHECK (LENGTH(content) > 0 AND LENGTH(content) <= 2200);

-- Valid departments
ALTER TABLE accounts_customuser ADD CONSTRAINT check_valid_department
CHECK (department IN (
    'Computer Science and Engineering',
    'Electrical and Electronic Engineering',
    'Business Administration',
    'English',
    'Law',
    'Architecture'
));
```

## 📊 Database Statistics and Monitoring

### Useful Statistics Queries

1. **User Activity Statistics**
   ```sql
   SELECT 
       department,
       COUNT(*) as total_users,
       COUNT(CASE WHEN last_login > NOW() - INTERVAL '30 days' THEN 1 END) as active_users,
       AVG(EXTRACT(DAYS FROM NOW() - date_joined)) as avg_days_since_joined
   FROM accounts_customuser
   GROUP BY department
   ORDER BY total_users DESC;
   ```

2. **Content Statistics**
   ```sql
   SELECT 
       DATE(created_at) as date,
       COUNT(*) as posts_count,
       COUNT(DISTINCT author_id) as unique_authors
   FROM social_post
   WHERE created_at > NOW() - INTERVAL '30 days'
   GROUP BY DATE(created_at)
   ORDER BY date DESC;
   ```

3. **Engagement Metrics**
   ```sql
   SELECT 
       p.id,
       p.content,
       COUNT(DISTINCT pl.user_id) as likes,
       COUNT(DISTINCT c.id) as comments,
       (COUNT(DISTINCT pl.user_id) + COUNT(DISTINCT c.id)) as total_engagement
   FROM social_post p
   LEFT JOIN social_post_likes pl ON p.id = pl.post_id
   LEFT JOIN social_comment c ON p.id = c.post_id
   WHERE p.created_at > NOW() - INTERVAL '7 days'
   GROUP BY p.id, p.content
   ORDER BY total_engagement DESC
   LIMIT 10;
   ```

## 🔄 Database Migrations

### Migration Strategy
```python
# Example migration for adding new field
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['department'], name='idx_user_department'),
        ),
    ]
```

### Data Migration Example
```python
from django.db import migrations

def update_department_names(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')
    CustomUser.objects.filter(department='CSE').update(
        department='Computer Science and Engineering'
    )

def reverse_department_names(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')
    CustomUser.objects.filter(
        department='Computer Science and Engineering'
    ).update(department='CSE')

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_add_phone_number'),
    ]

    operations = [
        migrations.RunPython(
            update_department_names,
            reverse_department_names
        ),
    ]
```

## 💾 Backup and Recovery

### Backup Strategy
```bash
# Full database backup
pg_dump -h localhost -U postgres -d greenlink > backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
pg_dump -h localhost -U postgres -d greenlink | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup with custom format (faster restore)
pg_dump -Fc -h localhost -U postgres -d greenlink > backup_$(date +%Y%m%d_%H%M%S).dump
```

### Recovery Commands
```bash
# Restore from SQL backup
psql -h localhost -U postgres -d greenlink < backup_20241019_120000.sql

# Restore from custom format
pg_restore -h localhost -U postgres -d greenlink backup_20241019_120000.dump
```

## 📈 Performance Tuning

### Database Configuration
```sql
-- PostgreSQL performance settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

### Query Performance Analysis
```sql
-- Enable query timing
\timing on

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM social_post WHERE author_id = 1;

-- Check slow queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

---

This database documentation provides comprehensive coverage of GreenLink's data architecture, optimization strategies, and maintenance procedures. Regular monitoring and optimization ensure optimal performance as the user base grows.
