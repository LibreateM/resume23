from django.db import models
from django.contrib.auth.models import User
import json


class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('minimal', 'Minimal'),
        ('executive', 'Executive'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, default='My Resume')
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')

    # Personal Info
    full_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    summary = models.TextField(blank=True)

    # JSON fields for dynamic sections
    education_data = models.TextField(default='[]')
    experience_data = models.TextField(default='[]')
    skills_data = models.TextField(default='[]')
    projects_data = models.TextField(default='[]')
    certifications_data = models.TextField(default='[]')

    is_ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def get_education(self):
        try:
            return json.loads(self.education_data)
        except:
            return []

    def get_experience(self):
        try:
            return json.loads(self.experience_data)
        except:
            return []

    def get_skills(self):
        try:
            return json.loads(self.skills_data)
        except:
            return []

    def get_projects(self):
        try:
            return json.loads(self.projects_data)
        except:
            return []

    def get_certifications(self):
        try:
            return json.loads(self.certifications_data)
        except:
            return []
