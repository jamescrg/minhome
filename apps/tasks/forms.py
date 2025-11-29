from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row
from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "folder",
            "title",
            "due_date",
            "due_time",
        )
        widgets = {
            "title": forms.TextInput(attrs={"tabindex": "2", "autofocus": True}),
            "due_date": forms.DateInput(attrs={"type": "date", "tabindex": "3"}),
            "due_time": forms.TimeInput(attrs={"type": "time", "tabindex": "4"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("folder", css_class="col-12 col-md-4"),
                Column("due_date", css_class="col-6 col-md-4"),
                Column("due_time", css_class="col-6 col-md-4"),
            ),
            Field("title"),
        )
