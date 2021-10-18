

from django import forms

from .models import Contact
            

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = (
                'folder', 
                'name', 
                'company',
                'address',
                'phone1',
                'phone1_label',
                'phone2',
                'phone2_label',
                'phone3',
                'phone3_label',
                'email',
                'notes',
                )
        PHONE_LABELS = (
                ('Mobile', 'Mobile'),
                ('Home', 'Home'),
                ('Work', 'Work'),
                ('Fax', 'Fax'),
                ('Other', 'Other'),
                )
        widgets = {
            'notes': forms.Textarea(),
            'phone1_label': forms.Select(choices=PHONE_LABELS),
            'phone2_label': forms.Select(choices=PHONE_LABELS),
            'phone3_label': forms.Select(choices=PHONE_LABELS),
        }
