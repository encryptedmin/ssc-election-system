from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from elections.models import Election
from elections.services import close_concluded_elections

from .forms import (
    CandidateForm,
    PositionForm,
)
from .models import (
    Candidate,
    Position,
)


@admin_required
def add_position(request, election_id):
    close_concluded_elections()

    election = get_object_or_404(
        Election,
        id=election_id
    )

    if election.is_concluded:

        messages.error(
            request,
            'Concluded elections cannot be edited.'
        )

        return redirect(
            'elections:election_detail',
            election_id=election.id
        )

    form = PositionForm(
        request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            position = form.save(
                commit=False
            )

            position.election = election

            position.save()

            return redirect(
                'elections:election_detail',
                election_id=election.id
            )

    return render(
        request,
        'candidates/add_position.html',
        {
            'form': form,
            'election': election,
        }
    )


@admin_required
def delete_position(request, position_id):
    close_concluded_elections()

    position = get_object_or_404(
        Position,
        id=position_id
    )

    election_id = position.election.id

    if position.election.is_concluded:

        messages.error(
            request,
            'Concluded elections cannot be edited.'
        )

        return redirect(
            'elections:election_detail',
            election_id=election_id
        )

    position.delete()

    return redirect(
        'elections:election_detail',
        election_id=election_id
    )


@admin_required
def manage_candidates(request, position_id):
    close_concluded_elections()

    position = get_object_or_404(
        Position,
        id=position_id
    )

    candidates = Candidate.objects.filter(
        position=position
    )

    context = {
        'position': position,
        'candidates': candidates,
    }

    return render(
        request,
        'candidates/manage_candidates.html',
        context
    )


@admin_required
def add_candidate(request, position_id):
    close_concluded_elections()

    position = get_object_or_404(
        Position,
        id=position_id
    )

    if position.election.is_concluded:

        messages.error(
            request,
            'Concluded elections cannot be edited.'
        )

        return redirect(
            'manage_candidates',
            position_id=position.id
        )

    form = CandidateForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == 'POST':

        if form.is_valid():

            candidate = form.save(
                commit=False
            )

            candidate.position = position

            candidate.election = position.election

            candidate.save()

            return redirect(
                'manage_candidates',
                position_id=position.id
            )

    return render(
        request,
        'candidates/add_candidate.html',
        {
            'form': form,
            'position': position,
        }
    )


@admin_required
def delete_candidate(request, candidate_id):
    close_concluded_elections()

    candidate = get_object_or_404(
        Candidate,
        id=candidate_id
    )

    position_id = candidate.position.id

    if candidate.election.is_concluded:

        messages.error(
            request,
            'Concluded elections cannot be edited.'
        )

        return redirect(
            'manage_candidates',
            position_id=position_id
        )

    candidate.delete()

    return redirect(
        'manage_candidates',
        position_id=position_id
    )
