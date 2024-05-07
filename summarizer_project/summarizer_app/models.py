from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title
