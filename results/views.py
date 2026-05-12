from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from elections.models import Election
from elections.services import close_concluded_elections

from .services import get_election_results


def _base_template(request):
    if getattr(request.user, 'role', None) == 'VOTER':
        return 'layouts/voter_base.html'

    return 'layouts/admin_base.html'


@login_required
def results_dashboard(request):
    close_concluded_elections()

    elections = Election.objects.annotate(
        vote_count=Count('vote', distinct=True),
        position_count=Count('position', distinct=True),
        candidate_count=Count('candidate', distinct=True),
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'results/results_dashboard.html',
        {
            'base_template': _base_template(request),
            'elections': elections,
        }
    )


@login_required
def election_results(request, election_id):
    close_concluded_elections()

    election = get_object_or_404(
        Election,
        id=election_id
    )

    return render(
        request,
        'results/election_results.html',
        {
            'base_template': _base_template(request),
            'election': election,
            'results': get_election_results(election),
        }
    )


@login_required
def election_results_data(request, election_id):
    close_concluded_elections()

    election = get_object_or_404(
        Election,
        id=election_id
    )

    return JsonResponse(
        get_election_results(election)
    )
