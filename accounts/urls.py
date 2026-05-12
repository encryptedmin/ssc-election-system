from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'admin-register/',
        views.admin_register_view,
        name='admin_register'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
]