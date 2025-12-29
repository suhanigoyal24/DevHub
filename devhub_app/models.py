from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------------
# 1. User Model
# -------------------------
class User(AbstractUser):
    # username, email, password already included in AbstractUser
    repositories = models.ManyToManyField('Repository', blank=True, related_name='users')
    followed_users = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    starred_repos = models.ManyToManyField('Repository', blank=True, related_name='starred_by')

    def __str__(self):
        return self.username

# -------------------------
# 2. Repository Model
# -------------------------
class Repository(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    content = models.JSONField(default=list, blank=True)  # List of file names or paths
    visibility = models.BooleanField(default=True)        # True = public, False = private
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_repos')
    
    def __str__(self):
        return self.name

# -------------------------
# 3. Issue Model
# -------------------------
class Issue(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.status})"
