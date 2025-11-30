from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import ValidationError

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = (
            "folder",
            "subject",
            "note",
        )
        widgets = {
            "note": forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout("subject", "note")

    def clean_subject(self):
        subject = self.cleaned_data["subject"]
        if len(subject) > 50:
            raise ValidationError("Subject must be fewer than 50 characters")
        return subject
