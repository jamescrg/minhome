
from django import forms

from .models import Favorite

class FavoriteForm(forms.ModelForm):


    class Meta:
        model = Favorite
        fields = (
                'folder', 
                'name', 
                'url', 
                'description',
                'login',
                'root',
                'passkey',
                )
        widgets = {
            'description': forms.Textarea(),
        }
