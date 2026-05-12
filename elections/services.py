from django.utils import timezone

from .models import Election


def close_concluded_elections():
    Election.objects.filter(
        is_active=True,
        end_time__lte=timezone.now()
    ).update(
        is_active=False
    )
