from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def total_resumes(self):
        return self.user.resumes.count()

    @property
    def avg_ats_score(self):
        checks = self.user.ats_checks.all()
        if checks.exists():
            return round(checks.aggregate(Avg('score'))['score__avg'], 1)
        return 0
