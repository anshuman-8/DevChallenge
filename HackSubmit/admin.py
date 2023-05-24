from django.contrib import admin

# Register your models here.

from .models import Hackathon, Submission

admin.site.register(Hackathon)
admin.site.register(Submission)