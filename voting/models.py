from django.db import models

from accounts.models import User
from candidates.models import Candidate, Position
from elections.models import Election


class Vote(models.Model):

    voter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'voter',
            'election',
            'position',
        )