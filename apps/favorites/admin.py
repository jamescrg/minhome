from django.contrib import admin

from .models import Favorite


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "folder", "name", "home_rank")


admin.site.register(Favorite, FavoriteAdmin)
