from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from candidates.models import Candidate, Position
from elections.models import Election
from elections.services import close_concluded_elections

from .models import Vote


@login_required
def election_list(request):
    close_concluded_elections()
    now = timezone.now()

    elections = Election.objects.filter(
        is_active=True,
        start_time__lte=now,
        end_time__gt=now
    )

    return render(
        request,
        'voting/election_list.html',
        {
            'elections': elections
        }
    )


@login_required
def election_ballot(request, election_id):
    close_concluded_elections()
    now = timezone.now()

    election = get_object_or_404(
        Election,
        id=election_id,
        is_active=True,
        start_time__lte=now,
        end_time__gt=now
    )

    positions = Position.objects.filter(
        election=election
    ).order_by('order')

    already_voted = Vote.objects.filter(
        voter=request.user,
        election=election
    ).exists()

    if already_voted:

        messages.info(
            request,
            'You already voted in this election.'
        )

        return redirect(
            'results:voter_results',
            election_id=election.id
        )

    context = {
        'election': election,
        'positions': positions,
    }

    return render(
        request,
        'voting/election_ballot.html',
        context
    )


@login_required
def submit_ballot(request, election_id):
    close_concluded_elections()
    now = timezone.now()

    election = get_object_or_404(
        Election,
        id=election_id,
        is_active=True,
        start_time__lte=now,
        end_time__gt=now
    )

    existing_vote = Vote.objects.filter(
        voter=request.user,
        election=election
    ).exists()

    if existing_vote:

        messages.error(
            request,
            'You already submitted your ballot.'
        )

        return redirect('voting:election_list')

    positions = Position.objects.filter(
        election=election
    )

    for position in positions:

        candidate_id = request.POST.get(
            f'position_{position.id}'
        )

        if not candidate_id:
            continue

        candidate = get_object_or_404(
            Candidate,
            id=candidate_id,
            position=position
        )

        Vote.objects.create(
            voter=request.user,
            election=election,
            position=position,
            candidate=candidate
        )

    messages.success(
        request,
        'Ballot submitted successfully.'
    )

    return redirect(
        'results:voter_results',
        election_id=election.id
    )
