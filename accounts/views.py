from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import (
    AdminRegisterForm,
    RegisterForm,
)


def login_view(request):

    if request.user.is_authenticated:

        if request.user.role in [
            'SUPER_ADMIN',
            'ADMIN',
        ]:
            return redirect('admin_dashboard')

        return redirect('voter_dashboard')

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            user = form.get_user()

            if not user.is_approved:

                messages.error(
                    request,
                    'Your account is pending approval.'
                )

                return redirect('login')

            login(request, user)

            if user.role in [
                'SUPER_ADMIN',
                'ADMIN',
            ]:
                return redirect('admin_dashboard')

            return redirect('voter_dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'registration/login.html',
        {
            'form': form
        }
    )


def register_view(request):

    form = RegisterForm(
        request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            user = form.save(commit=False)

            user.role = 'VOTER'

            user.is_approved = False

            user.save()

            messages.success(
                request,
                'Registration submitted successfully. Wait for admin approval.'
            )

            return redirect('login')

    return render(
        request,
        'registration/register.html',
        {
            'form': form
        }
    )


def admin_register_view(request):

    form = AdminRegisterForm(
        request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            admin = form.save(commit=False)

            admin.role = 'ADMIN'

            admin.is_approved = False

            admin.save()

            messages.success(
                request,
                'Admin registration submitted for approval.'
            )

            return redirect('login')

    return render(
        request,
        'registration/admin_register.html',
        {
            'form': form
        }
    )


def logout_view(request):

    logout(request)

    return redirect('landing_page')