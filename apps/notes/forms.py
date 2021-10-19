
from django import forms
from django.core.exceptions import ValidationError

from .models import Note

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('folder', 'subject', 'note',)
        widgets = {
            'note': forms.Textarea(),
        }

    def clean_subject(self):

        subject = self.cleaned_data['subject']

        if len(subject) < 2:
            raise ValidationError('Subject must be 2 or more characters')

        if len(subject) > 15:
            raise ValidationError('Subject must be fewer than 50 characters')

        return subject
