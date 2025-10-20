from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
import uuid

User = get_user_model()


class Post(models.Model):
    """Facebook-like posts with rich content and engagement features"""
    POST_TYPES = [
        ('status', 'Status Update'),
        ('photo', 'Photo Post'),
        ('video', 'Video Post'),
        ('project', 'Project Showcase'),
        ('achievement', 'Achievement'),
        ('job', 'Job/Internship'),
        ('academic', 'Academic Update'),
        ('event', 'Event'),
        ('poll', 'Poll'),
    ]
    
    REACTION_TYPES = [
        ('like', '👍 Like'),
        ('love', '❤️ Love'),
        ('haha', '😆 Haha'),
        ('wow', '😮 Wow'),
        ('sad', '😢 Sad'),
        ('angry', '😡 Angry'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=5000, blank=True)  # Facebook-like longer posts
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='status')
    
    # Media attachments (multiple files support)
    images = models.JSONField(default=list, blank=True)  # Store multiple image URLs
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    document = models.FileField(upload_to='post_documents/', blank=True, null=True)
    
    # Location and tagging
    location = models.CharField(max_length=255, blank=True)
    tagged_users = models.ManyToManyField(User, blank=True, related_name='tagged_in_posts')
    
    # Engagement metrics
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    reactions_count = models.JSONField(default=dict, blank=True)  # Count each reaction type
    
    # Visibility and moderation
    is_public = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    shared_from = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='shares')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.author.get_display_name}: {self.content[:50]}..."
    
    def get_absolute_url(self):
        return reverse('social:post_detail', kwargs={'pk': self.pk})
    
    def update_reaction_counts(self):
        """Update the reaction counts JSON field"""
        from django.db.models import Count
        reactions = self.reactions.values('reaction_type').annotate(count=Count('reaction_type'))
        self.reactions_count = {r['reaction_type']: r['count'] for r in reactions}
        self.save(update_fields=['reactions_count'])
    
    def get_top_reactions(self, limit=3):
        """Get the most popular reactions"""
        if not self.reactions_count:
            return []
        sorted_reactions = sorted(self.reactions_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_reactions[:limit]
    
    def user_reaction(self, user):
        """Get the user's reaction to this post"""
        try:
            return self.reactions.get(user=user).reaction_type
        except:
            return None
    
    def can_edit(self, user):
        """Check if user can edit this post"""
        return self.author == user or user.is_staff
    
    def get_share_text(self):
        """Get text for sharing"""
        if self.shared_from:
            return f"Shared from {self.shared_from.author.get_display_name}"
        return ""


class PostReaction(models.Model):
    """Facebook-style reactions (like, love, haha, etc.)"""
    REACTION_TYPES = [
        ('like', '👍 Like'),
        ('love', '❤️ Love'),
        ('haha', '😆 Haha'),
        ('wow', '😮 Wow'),
        ('sad', '😢 Sad'),
        ('angry', '😡 Angry'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update post's reaction counts
        self.post.update_reaction_counts()


class PostLike(models.Model):
    """Legacy like model - keeping for backward compatibility"""
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


class Story(models.Model):
    """Instagram/Facebook-like stories that disappear after 24 hours"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    content = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='story_images/', blank=True, null=True)
    video = models.FileField(upload_to='story_videos/', blank=True, null=True)
    background_color = models.CharField(max_length=7, default='#1877f2')  # Hex color
    
    views_count = models.PositiveIntegerField(default=0)
    viewers = models.ManyToManyField(User, blank=True, related_name='viewed_stories')
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Auto-calculated as 24 hours from creation
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'
    
    def __str__(self):
        return f"{self.author.get_display_name}'s story"
    
    def is_active(self):
        from django.utils import timezone
        return timezone.now() < self.expires_at
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            from django.utils import timezone
            from datetime import timedelta
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)


class Group(models.Model):
    """Facebook-like groups for departments, courses, interests"""
    GROUP_TYPES = [
        ('public', 'Public Group'),
        ('private', 'Private Group'),
        ('secret', 'Secret Group'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    cover_image = models.ImageField(upload_to='group_covers/', blank=True, null=True)
    group_type = models.CharField(max_length=10, choices=GROUP_TYPES, default='public')
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_social_groups')
    admins = models.ManyToManyField(User, related_name='admin_social_groups', blank=True)
    members = models.ManyToManyField(User, through='GroupMembership', related_name='joined_social_groups')
    
    members_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    """Group membership with roles"""
    MEMBER_ROLES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=MEMBER_ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'group')


class Event(models.Model):
    """Facebook-like events"""
    EVENT_TYPES = [
        ('academic', 'Academic Event'),
        ('social', 'Social Event'),
        ('career', 'Career Event'),
        ('sports', 'Sports Event'),
        ('cultural', 'Cultural Event'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    cover_image = models.ImageField(upload_to='event_covers/', blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='academic')
    
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    
    attendees = models.ManyToManyField(User, through='EventAttendance', related_name='attending_events')
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    
    is_public = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_datetime']
    
    def __str__(self):
        return self.title


class EventAttendance(models.Model):
    """Event attendance status"""
    ATTENDANCE_STATUS = [
        ('going', 'Going'),
        ('maybe', 'Maybe'),
        ('not_going', 'Not Going'),
        ('interested', 'Interested'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS, default='interested')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')


class FriendRequest(models.Model):
    """Facebook-like friend requests"""
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    message = models.TextField(max_length=300, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')
    
    def __str__(self):
        return f"{self.sender.get_display_name} -> {self.receiver.get_display_name} ({self.status})"


class Friendship(models.Model):
    """Facebook-like friendships"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
    
    def __str__(self):
        return f"{self.user1.get_display_name} ↔ {self.user2.get_display_name}"


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
