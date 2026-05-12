from django.urls import path

from . import views

urlpatterns = [

    path(
        'add-position/<int:election_id>/',
        views.add_position,
        name='add_position'
    ),

    path(
        'delete-position/<int:position_id>/',
        views.delete_position,
        name='delete_position'
    ),

    path(
        'manage/<int:position_id>/',
        views.manage_candidates,
        name='manage_candidates'
    ),

    path(
        'add-candidate/<int:position_id>/',
        views.add_candidate,
        name='add_candidate'
    ),

    path(
        'delete-candidate/<int:candidate_id>/',
        views.delete_candidate,
        name='delete_candidate'
    ),
]