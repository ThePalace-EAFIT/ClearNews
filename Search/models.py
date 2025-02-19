from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.


class New(models.Model):
    headline = models.CharField(max_length=100)
    body = models.CharField(max_length=250)
    date = models.DateTimeField(default=timezone.now)
    url = models.URLField(blank=True)
    credibility_score = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
