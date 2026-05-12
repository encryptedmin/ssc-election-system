from django import forms

from .models import Candidate, Position


class PositionForm(forms.ModelForm):

    class Meta:

        model = Position

        fields = [
            'name',
            'max_votes',
            'order',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Position Name',
                }
            ),

            'max_votes': forms.NumberInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Maximum Votes',
                }
            ),

            'order': forms.NumberInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Display Order',
                }
            ),
        }


class CandidateForm(forms.ModelForm):

    class Meta:

        model = Candidate

        fields = [
            'fullname',
            'photo',
            'platform',
        ]

        widgets = {

            'fullname': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Candidate Full Name',
                }
            ),

            'platform': forms.Textarea(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 h-32 resize-none focus:outline-none focus:border-blue-500',
                    'placeholder': 'Candidate Platform',
                }
            ),
        }