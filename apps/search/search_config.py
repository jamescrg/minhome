"""Watson search registration for global search models."""

from watson import search as watson

from apps.contacts.models import Contact
from apps.favorites.models import Favorite
from apps.notes.models import Note

# Register Favorite model for search
watson.register(
    Favorite,
    fields=("name", "url", "description"),
)


# Register Contact model for search
watson.register(
    Contact,
    fields=("name", "company", "email", "phone1", "phone2", "phone3", "notes"),
)

# Register Note model for search
watson.register(
    Note,
    fields=("title", "content"),
)
