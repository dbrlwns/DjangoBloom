from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        default="profile_images/2om.jpg" # Default value
    )