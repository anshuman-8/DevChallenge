from django.db import models
from django.contrib.auth.models import AbstractUser, User


# class User(AbstractUser):
#     uuid = models.UUIDField(primary_key=True)

#     def __str__(self):
#         return self.username


class Hackathon(models.Model):
    uuid = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    background_image = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    reward = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    HACKATHON_TYPES = [
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    ]

    type = models.CharField(max_length=10, choices=HACKATHON_TYPES, default='image', editable=False)

    def __str__(self):
        return self.title
    
    @property
    def hackathon_duration(self):
        return self.end_date - self.start_date
    
    @property
    def hackathon_duration_days(self):
        return self.hackathon_duration.days


class Submission(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    summary = models.TextField()

    def __str__(self):
        return self.name

    



