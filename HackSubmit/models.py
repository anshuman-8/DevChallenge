from django.db import models
from django.contrib.auth.models import User


class Hackathon(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    background_image = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    reward = models.CharField(max_length=100, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)

    HACKATHON_TYPES = [
        ("image", "Image"),
        ("file", "File"),
        ("link", "Link"),
    ]
    type = models.CharField(max_length=10, choices=HACKATHON_TYPES, default="image")

    def __str__(self):
        return self.title

    @property
    def hackathon_duration(self):
        return self.end_date - self.start_date

    @property
    def hackathon_duration_days(self):
        return self.hackathon_duration.days


class Submission(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="submissions/images/", null=True, blank=True)
    file = models.FileField(upload_to="submissions/files/", null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=100)
    summary = models.TextField()

    def __str__(self):
        return self.name

    @property
    def submission(self):
        if self.image:
            return self.image.url
        elif self.file:
            return self.file.url
        elif self.link:
            return self.link
        else:
            return None
