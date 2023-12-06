from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='user_images/')
    theme = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return self.user.username