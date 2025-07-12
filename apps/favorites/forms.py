from django import forms
from django.core.exceptions import ValidationError

from .models import Favorite


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = (
            "name",
            "url",
            "description",
        )
        widgets = {
            "description": forms.Textarea(),
        }

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


class FavoriteExtensionForm(FavoriteForm):
    class Meta:
        model = Favorite
        fields = (
            "folder",
            "name",
            "url",
            "description",
        )
        widgets = {
            "description": forms.Textarea(),
        }

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
