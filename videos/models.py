from django.db import models

class Video(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']