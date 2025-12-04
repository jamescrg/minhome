from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    RECURRENCE_CHOICES = [
        ("", "No recurrence"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    recurrence = forms.ChoiceField(
        choices=RECURRENCE_CHOICES,
        required=False,
        label="Repeat",
    )

    class Meta:
        model = Task
        fields = (
            "folder",
            "title",
            "due_date",
            "due_time",
        )
        widgets = {
            "title": forms.TextInput(attrs={"tabindex": "1", "autofocus": True}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "due_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial value for recurrence dropdown based on model fields
        if self.instance and self.instance.pk:
            if self.instance.is_recurring and self.instance.recurrence_type:
                self.fields["recurrence"].initial = self.instance.recurrence_type

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="col-12"),
            ),
            Row(
                Column("due_date", css_class="col-4"),
                Column("due_time", css_class="col-4"),
                Column("recurrence", css_class="col-4"),
            ),
        )
