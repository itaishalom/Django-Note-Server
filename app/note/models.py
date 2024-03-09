# note.py
from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    title2 = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    body = models.TextField()
    tags = models.CharField(
        max_length=255)  # Field to store comma-separated tags
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES,
                               default='public')

    def __str__(self):
        return self.title
