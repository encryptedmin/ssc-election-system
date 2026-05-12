from django.db import models

from elections.models import Election


class Position(models.Model):

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)

    order = models.PositiveIntegerField(default=0)

    max_votes = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class Candidate(models.Model):

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    fullname = models.CharField(max_length=255)

    photo = models.ImageField(
        upload_to='candidates/'
    )

    platform = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname