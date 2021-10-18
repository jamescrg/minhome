
from django import forms

from .models import Note

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('folder', 'subject', 'note',)
        widgets = {
            'note': forms.Textarea(),
        }
