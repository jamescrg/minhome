from django.contrib import admin

from .models import Folder


class FolderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "page",
        "parent",
        "home_column",
        "home_rank",
        "selected",
    )


admin.site.register(Folder, FolderAdmin)
