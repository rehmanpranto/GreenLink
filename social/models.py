from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
import uuid

User = get_user_model()


class Post(models.Model):
    """Twitter-like posts with additional professional features"""
    POST_TYPES = [
        ('post', 'Regular Post'),
        ('project', 'Project Showcase'),
        ('achievement', 'Achievement'),
        ('job', 'Job/Internship'),
        ('academic', 'Academic Update'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2200)  # Twitter-like character limit
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='post')
    
    # Media attachments
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    document = models.FileField(upload_to='post_documents/', blank=True, null=True)
    
    # Engagement metrics
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    # Visibility and moderation
    is_public = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.author.get_display_name}: {self.content[:50]}..."
    
    def get_absolute_url(self):
        return reverse('social:post_detail', kwargs={'pk': self.pk})


class PostLike(models.Model):
    """Twitter-like post likes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    """Comments on posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.get_display_name}: {self.content[:30]}..."


class Follow(models.Model):
    """Twitter-like follow system"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower.get_display_name} follows {self.following.get_display_name}"


class Hashtag(models.Model):
    """Twitter-like hashtag system"""
    name = models.CharField(max_length=100, unique=True)
    posts = models.ManyToManyField(Post, blank=True, related_name='hashtags')
    usage_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"#{self.name}"


class Experience(models.Model):
    """LinkedIn-like work experience"""
    EXPERIENCE_TYPES = [
        ('internship', 'Internship'),
        ('part_time', 'Part-time Job'),
        ('full_time', 'Full-time Job'),
        ('volunteer', 'Volunteer Work'),
        ('project', 'Project Work'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES)
    description = models.TextField(max_length=1000, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    """LinkedIn-like education information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    description = models.TextField(max_length=1000, blank=True)
    
    class Meta:
        ordering = ['-start_year']
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Skill(models.Model):
    """LinkedIn-like skills"""
    SKILL_CATEGORIES = [
        ('technical', 'Technical Skills'),
        ('soft', 'Soft Skills'),
        ('language', 'Languages'),
        ('academic', 'Academic Skills'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, default='technical')
    users = models.ManyToManyField(User, through='UserSkill', related_name='skills')
    
    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """User-skill relationship with endorsements"""
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=15, choices=PROFICIENCY_LEVELS, default='intermediate')
    endorsements_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'skill')


class SkillEndorsement(models.Model):
    """LinkedIn-like skill endorsements"""
    endorser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_endorsements')
    user_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE, related_name='endorsements')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('endorser', 'user_skill')


class Connection(models.Model):
    """LinkedIn-like professional connections"""
    CONNECTION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=10, choices=CONNECTION_STATUS, default='pending')
    message = models.TextField(max_length=300, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')
    
    def __str__(self):
        return f"{self.sender.get_display_name} -> {self.receiver.get_display_name} ({self.status})"


class StudyGroup(models.Model):
    """Academic study groups"""
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    course_code = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='study_groups')
    
    max_members = models.PositiveIntegerField(default=20)
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        return self.members.count()


class Notification(models.Model):
    """Twitter/LinkedIn-like notifications"""
    NOTIFICATION_TYPES = [
        ('like', 'Post Liked'),
        ('comment', 'New Comment'),
        ('follow', 'New Follower'),
        ('connection', 'Connection Request'),
        ('endorsement', 'Skill Endorsed'),
        ('mention', 'Mentioned in Post'),
        ('group_invite', 'Study Group Invite'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient.get_display_name}: {self.message}"
