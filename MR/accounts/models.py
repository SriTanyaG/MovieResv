from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    IS_THEATER_OWNER = 'theater_owner'
    IS_CUSTOMER = 'customer'
    
    ROLE_CHOICES = [
        (IS_THEATER_OWNER, 'Theater Owner'),
        (IS_CUSTOMER, 'Customer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=IS_CUSTOMER)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
