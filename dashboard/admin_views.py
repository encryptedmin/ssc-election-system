from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import super_admin_required
from accounts.models import User


@super_admin_required
def approval_dashboard(request):

    pending_voters = User.objects.filter(
        role='VOTER',
        is_approved=False
    )

    pending_admins = User.objects.filter(
        role='ADMIN',
        is_approved=False
    )

    context = {
        'pending_voters': pending_voters,
        'pending_admins': pending_admins,
    }

    return render(
        request,
        'dashboard/approval_dashboard.html',
        context
    )


@super_admin_required
def approve_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.is_approved = True

    user.save()

    return redirect('approval_dashboard')

@super_admin_required
def reject_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.delete()

    return redirect(
        'approval_dashboard'
    )