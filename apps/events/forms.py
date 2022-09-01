from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'date',
            'description',
            'status',
        )
        STATUSES = (
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Missed', 'Missed'),
        )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'autofocus': 'autofocus'}),
            'status': forms.Select(choices=STATUSES),
        }
