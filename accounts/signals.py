from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import User


@receiver(post_migrate)
def create_super_admin(sender, **kwargs):

    if not User.objects.filter(
        role='SUPER_ADMIN'
    ).exists():

        User.objects.create_superuser(
            username='masteradmin',
            email='admin@ssc.local',
            password='admin12345',
            role='SUPER_ADMIN',
            is_approved=True,
        )

        print(
            'Default SUPER_ADMIN created.'
        )