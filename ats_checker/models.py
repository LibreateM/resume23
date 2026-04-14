from django.db import models
from django.contrib.auth.models import User
from resumes.models import Resume


class ATSCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ats_checks')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True, related_name='ats_checks')
    resume_text = models.TextField(blank=True)
    job_description = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    feedback = models.TextField(blank=True)
    keywords_found = models.TextField(default='[]')
    keywords_missing = models.TextField(default='[]')
    suggestions = models.TextField(default='[]')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"ATS Check - {self.user.username} - Score: {self.score}"

    import json as _json
    def get_keywords_found(self):
        import json
        try: return json.loads(self.keywords_found)
        except: return []

    def get_keywords_missing(self):
        import json
        try: return json.loads(self.keywords_missing)
        except: return []

    def get_suggestions(self):
        import json
        try: return json.loads(self.suggestions)
        except: return []

    @property
    def score_label(self):
        if self.score >= 80: return 'Excellent'
        elif self.score >= 60: return 'Good'
        elif self.score >= 40: return 'Average'
        else: return 'Poor'

    @property
    def score_color(self):
        if self.score >= 80: return '#48c78e'
        elif self.score >= 60: return '#f5a623'
        elif self.score >= 40: return '#ffb347'
        else: return '#ff6b6b'
