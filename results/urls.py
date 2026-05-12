from django.urls import path

from . import views

app_name = 'results'

urlpatterns = [

    path(
        '',
        views.results_dashboard,
        name='results_dashboard'
    ),

    path(
        '<int:election_id>/data/',
        views.election_results_data,
        name='election_results_data'
    ),

    path(
        '<int:election_id>/',
        views.election_results,
        name='election_results'
    ),

    path(
        'voter/<int:election_id>/',
        views.election_results,
        name='voter_results'
    ),
]
