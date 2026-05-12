from django.urls import path

from . import admin_views, views

urlpatterns = [
    path(
        '',
        views.landing_page,
        name='landing_page'
    ),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'voter-dashboard/',
        views.voter_dashboard,
        name='voter_dashboard'
    ),

    path(
        'approvals/',
        admin_views.approval_dashboard,
        name='approval_dashboard'
    ),

    path(
        'approve-user/<int:user_id>/',
        admin_views.approve_user,
        name='approve_user'
    ),

    path(
    'reject-user/<int:user_id>/',
    admin_views.reject_user,
    name='reject_user'
    ),
]