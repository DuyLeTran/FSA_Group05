# team/models.py
from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
