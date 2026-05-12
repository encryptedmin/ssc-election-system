from django import forms

from .models import Election


class ElectionForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            self.add_error(
                'end_time',
                'End time must be after the start time.'
            )

        return cleaned_data

    class Meta:

        model = Election

        fields = [
            'title',
            'description',
            'start_time',
            'end_time',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                    'placeholder': 'Election Title',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500 h-32 resize-none',
                    'placeholder': 'Election Description',
                }
            ),

            'start_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                }
            ),

            'end_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3 focus:outline-none focus:border-blue-500',
                }
            ),
        }
