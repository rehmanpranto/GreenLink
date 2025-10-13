from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from social.models import Post, Hashtag
from datetime import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a test user for GreenLink platform'

    def handle(self, *args, **options):
        # Check if test user already exists
        if User.objects.filter(email='202310001@student.green.edu.bd').exists():
            user = User.objects.get(email='202310001@student.green.edu.bd')
            self.stdout.write(
                self.style.WARNING('Test user already exists!')
            )
        else:
            # Create test user
            user = User.objects.create_user(
                username='202310001',
                email='202310001@student.green.edu.bd',
                password='greenlink123',
                first_name='Ahmed',
                last_name='Rahman',
                student_id='202310001',
                department='CSE',
                batch='Fall 2023',
                phone_number='01712345678',
                headline='Computer Science Student | AI Enthusiast',
                bio='Passionate about technology and innovation. Love coding and solving complex problems.',
                linkedin_url='https://linkedin.com/in/ahmed-rahman',
                github_username='ahmed_rahman',
                gpa=3.75,
                graduation_year=2026,
                is_verified=True
            )
            
            self.stdout.write(
                self.style.SUCCESS('Test user created successfully!')
            )
        
        # Create some sample posts
        sample_posts = [
            {
                'content': 'Excited to join GreenLink! Looking forward to connecting with fellow Green University students! 🎓 #GreenUniversity #NewStudent',
                'post_type': 'text'
            },
            {
                'content': 'Just finished my Machine Learning assignment. The algorithms are fascinating! Anyone else working on AI projects? #MachineLearning #AI #CSE',
                'post_type': 'text'
            },
            {
                'content': 'Beautiful campus today! Green University really lives up to its name 🌿 #CampusLife #GreenUniversity',
                'post_type': 'text'
            }
        ]
        
        for post_data in sample_posts:
            if not Post.objects.filter(author=user, content=post_data['content']).exists():
                post = Post.objects.create(
                    author=user,
                    content=post_data['content'],
                    post_type=post_data['post_type']
                )
                
                # Extract and create hashtags
                words = post_data['content'].split()
                for word in words:
                    if word.startswith('#'):
                        hashtag_name = word[1:].lower()
                        hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
                        post.hashtags.add(hashtag)
        
        # Display account details
        self.stdout.write(
            self.style.SUCCESS('\n' + '='*50)
        )
        self.stdout.write(
            self.style.SUCCESS('TEST ACCOUNT DETAILS')
        )
        self.stdout.write(
            self.style.SUCCESS('='*50)
        )
        self.stdout.write(f'Email: 202310001@student.green.edu.bd')
        self.stdout.write(f'Password: greenlink123')
        self.stdout.write(f'Name: {user.first_name} {user.last_name}')
        self.stdout.write(f'Student ID: {user.student_id}')
        self.stdout.write(f'Department: {user.department}')
        self.stdout.write(f'GPA: {user.gpa}')
        self.stdout.write(
            self.style.SUCCESS('='*50)
        )
        self.stdout.write(
            self.style.SUCCESS('Login at: http://127.0.0.1:8000/accounts/login/')
        )
        self.stdout.write(
            self.style.SUCCESS('='*50)
        )
