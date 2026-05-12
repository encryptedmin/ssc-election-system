from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = [
            'student_id',
            'username',
            'email',
            'department',
            'year_level',
            'password1',
            'password2',
        ]

        widgets = {
            'student_id': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Student ID',
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Username',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Email',
                }
            ),

            'department': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Department',
                }
            ),

            'year_level': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Year Level',
                }
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                'placeholder': 'Password',
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                'placeholder': 'Confirm Password',
            }
        )
    )


class AdminRegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Username',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Email',
                }
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                'placeholder': 'Password',
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                'placeholder': 'Confirm Password',
            }
        )
    )