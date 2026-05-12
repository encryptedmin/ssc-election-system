from django.db import models
from django.utils import timezone


class Election(models.Model):

    title = models.CharField(max_length=255)

    description = models.TextField()

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def has_started(self):
        return timezone.now() >= self.start_time

    @property
    def has_ended(self):
        return timezone.now() >= self.end_time

    @property
    def is_concluded(self):
        return self.has_ended

    @property
    def is_open(self):
        now = timezone.now()

        return (
            self.is_active and
            self.start_time <= now < self.end_time
        )

    @property
    def status_label(self):
        if self.is_concluded:
            return 'Concluded'

        if self.is_open:
            return 'Active'

        if self.is_active:
            return 'Scheduled'

        return 'Draft'

    def __str__(self):
        return self.title
