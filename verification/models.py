from django.db import models
from django.contrib.auth.models import User

class AnalyzedNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    text = models.TextField()
    score = models.IntegerField()
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.score})"