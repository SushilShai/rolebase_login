from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, unique=True)

    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Housekeeper', 'Housekeeper'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
