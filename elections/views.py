from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from candidates.models import Candidate, Position

from .forms import ElectionForm
from .models import Election
from .services import close_concluded_elections


@admin_required
def election_list(request):
    close_concluded_elections()

    elections = Election.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'elections/election_list.html',
        {
            'elections': elections
        }
    )


@admin_required
def create_election(request):

    form = ElectionForm(
        request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            form.save()

            return redirect('elections:election_list')

    return render(
        request,
        'elections/create_election.html',
        {
            'form': form
        }
    )


@admin_required
def election_detail(request, election_id):
    close_concluded_elections()

    election = get_object_or_404(
        Election,
        id=election_id
    )

    positions = Position.objects.filter(
        election=election
    ).order_by('order')

    context = {
        'election': election,
        'positions': positions,
    }

    return render(
        request,
        'elections/election_detail.html',
        context
    )


@admin_required
def publish_election(request, election_id):
    close_concluded_elections()

    election = get_object_or_404(
        Election,
        id=election_id
    )

    if request.method != 'POST':

        messages.error(
            request,
            'Use the publish button to publish an election.'
        )

        return redirect(
            'elections:election_detail',
            election_id=election.id
        )

    if election.is_concluded:

        messages.error(
            request,
            'Concluded elections cannot be published again.'
        )

        return redirect(
            'elections:election_detail',
            election_id=election.id
        )

    positions = Position.objects.filter(
        election=election
    )

    if not positions.exists():

        messages.error(
            request,
            'Election must contain positions before publishing.'
        )

        return redirect(
            'elections:election_detail',
            election_id=election.id
        )

    for position in positions:

        has_candidates = Candidate.objects.filter(
            position=position
        ).exists()

        if not has_candidates:

            messages.error(
                request,
                f'{position.name} has no candidates.'
            )

            return redirect(
                'elections:election_detail',
                election_id=election.id
            )

    election.is_active = True

    election.save()

    messages.success(
        request,
        'Election published successfully.'
    )

    return redirect(
        'elections:election_detail',
        election_id=election.id
    )


@admin_required
def delete_election(request, election_id):
    close_concluded_elections()

    election = get_object_or_404(
        Election,
        id=election_id
    )

    if not election.is_concluded:

        messages.error(
            request,
            'Only concluded elections can be deleted.'
        )

        return redirect(
            'elections:election_detail',
            election_id=election.id
        )

    if request.method == 'POST':

        confirmation = request.POST.get(
            'confirmation',
            ''
        ).strip()
        acknowledged = request.POST.get('acknowledged') == 'on'

        if confirmation != election.title or not acknowledged:

            messages.error(
                request,
                'Deletion cancelled. Confirm the warning and type the exact election title.'
            )

            return redirect(
                'elections:delete_election',
                election_id=election.id
            )

        election_title = election.title
        election.delete()

        messages.success(
            request,
            f'{election_title} was deleted.'
        )

        return redirect('elections:election_list')

    return render(
        request,
        'elections/delete_election.html',
        {
            'election': election,
        }
    )
