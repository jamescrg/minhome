from django import forms

from apps.folders.folders import get_folders_for_page
from config.settings import CustomFormRenderer

from .models import Note


class NoteForm(forms.ModelForm):
    default_renderer = CustomFormRenderer
    use_required_attribute = False

    class Meta:
        model = Note
        fields = ("folder", "title")
        widgets = {
            "title": forms.TextInput(attrs={"class": "span2"}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)

        if request:
            self.fields["folder"].queryset = get_folders_for_page(request, "notes")

    def __iter__(self):
        for field in super().__iter__():
            if field.name != "folder":
                yield field
