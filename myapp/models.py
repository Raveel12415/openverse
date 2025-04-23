from django.db import models
from django.contrib.auth.models import User

class Signup1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.user.username
