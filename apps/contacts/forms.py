import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from config.settings import CustomFormRenderer

from .models import Contact


def normalize_phone(value):
    """
    Normalize phone to raw digits with optional extension.
    Returns (normalized_value, is_valid).

    Examples:
        "(406) 363-1234" -> ("4063631234", True)
        "1-406-363-1234" -> ("4063631234", True)
        "406.363.1234 x123" -> ("4063631234x123", True)
        "invalid" -> ("invalid", False)
    """
    if not value:
        return value, True

    value = value.strip()

    # Extract extension if present
    extension = ""
    ext_patterns = [" x ", " x", " ext", " ext.", ",", "x"]
    lower = value.lower()
    for pattern in ext_patterns:
        if pattern in lower:
            idx = lower.index(pattern)
            ext_part = value[idx:].lower()
            # Extract just the digits from extension
            ext_digits = "".join(c for c in ext_part if c.isdigit())
            if ext_digits:
                extension = f"x{ext_digits}"
            value = value[:idx]
            break

    # Strip all non-numeric characters
    digits = "".join(c for c in value if c.isdigit())

    # Handle +1 country code
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    # Validate: must be exactly 10 digits
    if len(digits) == 10:
        return digits + extension, True

    # Invalid - return original
    return value.strip() + (" " + extension if extension else ""), False


class ContactForm(forms.ModelForm):
    default_renderer = CustomFormRenderer
    use_required_attribute = False

    class Meta:
        model = Contact

        fields = (
            "folder",
            "name",
            "company",
            "address",
            "phone1",
            "phone1_label",
            "phone2",
            "phone2_label",
            "phone3",
            "phone3_label",
            "email",
            "website",
            "notes",
        )

        PHONE_LABELS = (
            ("Mobile", "Mobile"),
            ("Home", "Home"),
            ("Work", "Work"),
            ("Fax", "Fax"),
            ("Other", "Other"),
        )

        labels = {
            "phone1": "Phone",
            "phone1_label": "For",
            "phone2": "Phone 2",
            "phone2_label": "For",
            "phone3": "Phone 3",
            "phone3_label": "For",
        }

        widgets = {
            "address": forms.Textarea(attrs={"class": "span2"}),
            "notes": forms.Textarea(attrs={"class": "span2"}),
            "phone1_label": forms.Select(choices=PHONE_LABELS),
            "phone2_label": forms.Select(choices=PHONE_LABELS),
            "phone3_label": forms.Select(choices=PHONE_LABELS),
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

    def clean_company(self):
        company = self.cleaned_data["company"]
        if company:
            if len(company) >= 50:
                raise ValidationError("Company must be fewer than 50 characters.")
        return company

    def clean_address(self):
        address = self.cleaned_data["address"]
        if address:
            if len(address) > 250:
                raise ValidationError("Address must be fewer than 250 characters.")
        return address

    def clean_phone1(self):
        phone1 = self.cleaned_data["phone1"]
        if phone1:
            normalized, valid = normalize_phone(phone1)
            if not valid:
                raise ValidationError("Enter a valid 10-digit US phone number.")
            return normalized
        return phone1

    def clean_phone2(self):
        phone2 = self.cleaned_data["phone2"]
        if phone2:
            normalized, valid = normalize_phone(phone2)
            if not valid:
                raise ValidationError("Enter a valid 10-digit US phone number.")
            return normalized
        return phone2

    def clean_phone3(self):
        phone3 = self.cleaned_data["phone3"]
        if phone3:
            normalized, valid = normalize_phone(phone3)
            if not valid:
                raise ValidationError("Enter a valid 10-digit US phone number.")
            return normalized
        return phone3

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email:
            email = email.lower()
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError("Invalid email address.")
        return email

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            website = website.strip()
            if not website.startswith(("http://", "https://")):
                website = "https://" + website
            url_pattern = re.compile(
                r"^https?://"
                r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
                r"[a-zA-Z]{2,}"
                r"(?:/[^\s]*)?$"
            )
            if not url_pattern.match(website):
                raise ValidationError("Enter a valid website URL.")
        return website

    def clean_notes(self):
        notes = self.cleaned_data["notes"]
        if notes:
            if len(notes) >= 250:
                raise ValidationError("Notes must be fewer than 250 characters.")
        return notes
