from django.urls import path

from . import views

app_name = 'voting'

urlpatterns = [

    path(
        '',
        views.election_list,
        name='election_list'
    ),

    path(
        'ballot/<int:election_id>/',
        views.election_ballot,
        name='election_ballot'
    ),

    path(
        'submit/<int:election_id>/',
        views.submit_ballot,
        name='submit_ballot'
    ),
]