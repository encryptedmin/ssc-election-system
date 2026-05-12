from django.contrib import messages
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import super_admin_required
from accounts.models import User


@super_admin_required
def approval_dashboard(request):

    pending_voters = User.objects.filter(
        role='VOTER',
        is_approved=False
    ).order_by('created_at')

    pending_admins = User.objects.filter(
        role='ADMIN',
        is_approved=False
    ).order_by('created_at')

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
@require_POST
def approve_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.is_approved = True

    user.save()

    messages.success(
        request,
        f'{user.username} has been approved as {user.get_role_display()}.'
    )

    return redirect('approval_dashboard')

@super_admin_required
@require_POST
def reject_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    username = user.username
    role = user.get_role_display()

    user.delete()

    messages.success(
        request,
        f'{username} was rejected and removed from pending {role} accounts.'
    )

    return redirect(
        'approval_dashboard'
    )
