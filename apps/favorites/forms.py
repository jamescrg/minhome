from django import forms
from django.core.exceptions import ValidationError

from config.settings import CustomFormRenderer

from .models import Favorite


class FavoriteExtensionForm(forms.ModelForm):
    """Form for adding favorites via browser extension."""

    default_renderer = CustomFormRenderer

    class Meta:
        model = Favorite
        fields = ("folder", "name", "url")


class FavoriteForm(forms.ModelForm):
    default_renderer = CustomFormRenderer
    use_required_attribute = False

    class Meta:
        model = Favorite
        fields = (
            "folder",
            "name",
            "url",
            "description",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "span2"}),
            "url": forms.TextInput(attrs={"class": "span2"}),
            "description": forms.Textarea(attrs={"class": "span2"}),
        }

    def __iter__(self):
        for field in super().__iter__():
            if field.name != "folder":
                yield field

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise ValidationError("Name must be greater than 2 characters")
        if len(name) > 50:
            raise ValidationError("Name must be fewer than 50 characters")
        return name

    def clean_url(self):
        url = self.cleaned_data["url"]
        if url:
            if len(url) >= 250:
                raise ValidationError("Url must be fewer than 250 characters.")
        return url

    def clean_description(self):
        description = self.cleaned_data["description"]
        if description:
            if len(description) > 250:
                raise ValidationError("Description must be fewer than 250 characters.")
        return description
