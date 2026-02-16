from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms

from apps.folders.folders import get_folders_for_page

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("folder", "title")

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout("title")

        if request:
            self.fields["folder"].queryset = get_folders_for_page(request, "notes")
