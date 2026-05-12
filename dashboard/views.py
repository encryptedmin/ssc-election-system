from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from accounts.models import User
from candidates.models import Candidate
from elections.models import Election
from elections.services import close_concluded_elections
from voting.models import Vote
from accounts.decorators import admin_required


def landing_page(request):

    return render(
        request,
        'landing/index.html'
    )


@admin_required
def admin_dashboard(request):
    close_concluded_elections()
    now = timezone.now()

    context = {
        'total_voters': User.objects.filter(
            role='VOTER'
        ).count(),

        'total_votes': Vote.objects.count(),

        'total_candidates': Candidate.objects.count(),

        'active_elections': Election.objects.filter(
            is_active=True,
            start_time__lte=now,
            end_time__gt=now
        ).count(),
    }

    return render(
        request,
        'dashboard/admin_dashboard.html',
        context
    )


@login_required
def voter_dashboard(request):

    return render(
        request,
        'dashboard/voter_dashboard.html'
    )
