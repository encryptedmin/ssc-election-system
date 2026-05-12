from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.voter_list,
        name='voter_list'
    ),

    path(
        'edit/<int:voter_id>/',
        views.edit_voter,
        name='edit_voter'
    ),

    path(
        'delete/<int:voter_id>/',
        views.delete_voter,
        name='delete_voter'
    ),
]