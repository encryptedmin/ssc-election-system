from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from accounts.models import User


@admin_required
def voter_list(request):

    voters = User.objects.filter(
        role='VOTER'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'voters/voter_list.html',
        {
            'voters': voters
        }
    )


@admin_required
def edit_voter(request, voter_id):

    voter = get_object_or_404(
        User,
        id=voter_id,
        role='VOTER'
    )

    if request.method == 'POST':

        voter.username = request.POST.get(
            'username'
        )

        voter.email = request.POST.get(
            'email'
        )

        voter.student_id = request.POST.get(
            'student_id'
        )

        voter.department = request.POST.get(
            'department'
        )

        voter.year_level = request.POST.get(
            'year_level'
        )

        voter.save()

        return redirect('voter_list')

    return render(
        request,
        'voters/edit_voter.html',
        {
            'voter': voter
        }
    )


@admin_required
def delete_voter(request, voter_id):

    voter = get_object_or_404(
        User,
        id=voter_id,
        role='VOTER'
    )

    voter.delete()

    return redirect('voter_list')