from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class CivicIssue(models.Model):
    CATEGORY_CHOICES = [
        ('road', 'Road'),
        ('electric_line', 'Electric Line'),
        ('plumbing', 'Plumbing'),
        ('garbage', 'Garbage'),
        ('drainage', 'Drainage'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=False, null=False)
    custom_category = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=False, null=False)  # Make subject nullable
    description = models.TextField(blank=False, null=False)
    media = models.FileField(upload_to='issue_media/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True) 
    latitude = models.FloatField(null=True, blank=True)  # Allow latitude to be nullable
    longitude = models.FloatField(null=True, blank=True)  # Allow longitude to be nullable
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"
