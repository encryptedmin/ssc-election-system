from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('VOTER', 'Voter'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='VOTER'
    )

    student_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    department = models.CharField(
        max_length=255,
        blank=True
    )

    year_level = models.CharField(
        max_length=50,
        blank=True
    )

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_super_admin(self):
        return self.role == 'SUPER_ADMIN'

    def is_admin(self):
        return self.role in [
            'SUPER_ADMIN',
            'ADMIN'
        ]

    def __str__(self):
        return f'{self.username} ({self.role})'