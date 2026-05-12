from django.urls import path

from . import views

app_name = 'elections'

urlpatterns = [

    path(
        '',
        views.election_list,
        name='election_list'
    ),

    path(
        'create/',
        views.create_election,
        name='create_election'
    ),

    path(
        '<int:election_id>/',
        views.election_detail,
        name='election_detail'
    ),

    path(
        'publish/<int:election_id>/',
        views.publish_election,
        name='publish_election'
    ),

    path(
        'delete/<int:election_id>/',
        views.delete_election,
        name='delete_election'
    ),
]
