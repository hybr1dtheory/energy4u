from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    avg_result = models.FloatField(default=0)  # average result of all tests
    rating = models.FloatField(default=1.0)  # rating based on user activities

    def __str__(self):
        return f'{self.user.username} Profile'
