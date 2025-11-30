from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from apps.contacts import views as contacts
from apps.favorites import views as favorites
from apps.finance import views as finance
from apps.folders import views as folders
from apps.home import views as home
from apps.lab import views as lab
from apps.notes import views as notes
from apps.search import views as search
from apps.settings import views as settings
from apps.tasks import views as tasks
from apps.weather import views as weather

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    # folders
    path("folders/home/<int:id>/<str:page>", folders.home, name="folder-home"),
    path("folders/<int:id>/<str:page>", folders.select, name="folder-select"),
    path("folders/insert/<str:page>", folders.insert, name="folder-insert"),
    path("folders/update/<int:id>/<str:page>", folders.update, name="folder-update"),
    path("folders/delete/<int:id>/<str:page>", folders.delete, name="folder-delete"),
    path("folders/share/<int:id>/<str:page>", folders.share, name="folder-share"),
    # home
    path("", home.index, name="home-index"),
    path("home/", home.index, name="home"),
    path("home/folder/<int:id>/<str:direction>/", home.folder, name="home-folder"),
    path(
        "home/favorite/<int:id>/<str:direction>/", home.favorite, name="home-favorite"
    ),
    path("home/toggle/<str:section>", home.toggle, name="home-toggle"),
    path(
        "home/update-folder-column/",
        home.update_folder_column,
        name="home-update-folder-column",
    ),
    path(
        "home/swap-folder-positions/",
        home.swap_folder_positions,
        name="home-swap-folder-positions",
    ),
    path(
        "home/insert-folder-at-position/",
        home.insert_folder_at_position,
        name="home-insert-folder-at-position",
    ),
    path(
        "home/swap-favorite-positions/",
        home.swap_favorite_positions,
        name="home-swap-favorite-positions",
    ),
    path(
        "home/insert-favorite-at-position/",
        home.insert_favorite_at_position,
        name="home-insert-favorite-at-position",
    ),
    path(
        "home/move-favorite-to-folder/",
        home.move_favorite_to_folder,
        name="home-move-favorite-to-folder",
    ),
    # favorites
    path("favorites/", favorites.index, name="favorites"),
    path("favorites/add", favorites.add, name="favorites-add"),
    path("favorites/<int:id>/edit", favorites.edit, name="favorites-edit"),
    path("favorites/delete/<int:id>", favorites.delete, name="favorites-delete"),
    path("favorites/home/<int:id>", favorites.home, name="favorites-home"),
    path("favorites/api/add", favorites.api_add, name="favorites-api-add"),
    path("favorites/api/folders", favorites.api_folders, name="favorites-api-folders"),
    path("favorites/extension", favorites.extension_add, name="favorites-extension"),
    # tasks
    path("tasks/", tasks.index, name="tasks"),
    path("tasks/add", tasks.add, name="tasks-add"),
    path("tasks/<int:id>/edit", tasks.edit, name="tasks-edit"),
    path("tasks/<int:id>/delete", tasks.delete, name="tasks-delete"),
    path("tasks/<int:id>/complete", tasks.status, name="tasks-complete"),
    path("tasks/<int:id>/complete/<str:origin>", tasks.status, name="tasks-complete"),
    path("tasks/clear", tasks.clear, name="tasks-clear"),
    path(
        "tasks/add-editor/<int:folder_id>/<int:user_id>",
        tasks.add_editor,
        name="folder-add-editor",
    ),
    path(
        "tasks/remove-editor/<int:folder_id>/<int:user_id>",
        tasks.remove_editor,
        name="folder-remove-editor",
    ),
    # contacts
    path("contacts/", contacts.index, name="contacts"),
    path("contacts/<int:id>", contacts.select, name="contacts-select"),
    path("contacts/add", contacts.add, name="contacts-add"),
    path("contacts/<int:id>/edit", contacts.edit, name="contacts-edit"),
    path("contacts/<int:id>/delete", contacts.delete, name="contacts-delete"),
    path(
        "contacts/<int:id>/google-toggle",
        contacts.google_toggle,
        name="contacts-google-toggle",
    ),
    path("contacts/google-list", contacts.google_list, name="contacts-google-list"),
    # notes
    path("notes/", notes.index, name="notes"),
    path("notes/<int:id>", notes.select, name="notes-select"),
    path("notes/add", notes.add, name="notes-add"),
    path("notes/<int:id>/edit", notes.edit, name="notes-edit"),
    path("notes/<int:id>/delete", notes.delete, name="notes-delete"),
    # weather
    path("weather/", weather.index, name="weather"),
    path("weather/zip", weather.zip, name="weather-zip"),
    # finance
    path("crypto/", finance.crypto, name="crypto"),
    path("crypto/<str:ord>", finance.crypto, name="crypto"),
    path("securities/", finance.securities, name="securities"),
    path("securities/<str:ord>", finance.securities, name="securities"),
    path("positions/", finance.positions, name="positions"),
    # search
    path("search/", search.index, name="search"),
    path("search/results", search.results, name="search-results"),
    # settings
    path("settings/", settings.index, name="settings"),
    path("settings/google/login", settings.google_login, name="settings-google-login"),
    path("settings/google/store", settings.google_store, name="settings-google-store"),
    path(
        "settings/google/logout", settings.google_logout, name="settings-google-logout"
    ),
    path("settings/theme", settings.theme, name="settings-theme"),
    path(
        "settings/search-engine", settings.search_engine, name="settings-search-engine"
    ),
    path(
        "settings/home-options/<str:option>/<str:value>",
        settings.home_options,
        name="settings-home-options",
    ),
    path(
        "settings/crypto-symbols/",
        settings.crypto_symbols,
        name="settings-crypto-symbols",
    ),
    path(
        "settings/crypto-symbols/add",
        settings.crypto_symbol_add,
        name="settings-crypto-symbol-add",
    ),
    path(
        "settings/crypto-symbols/<int:id>/edit",
        settings.crypto_symbol_edit,
        name="settings-crypto-symbol-edit",
    ),
    path(
        "settings/crypto-symbols/<int:id>/delete",
        settings.crypto_symbol_delete,
        name="settings-crypto-symbol-delete",
    ),
    path(
        "settings/securities-symbols/",
        settings.securities_symbols,
        name="settings-securities-symbols",
    ),
    path(
        "settings/securities-symbols/add",
        settings.securities_symbol_add,
        name="settings-securities-symbol-add",
    ),
    path(
        "settings/securities-symbols/<int:id>/edit",
        settings.securities_symbol_edit,
        name="settings-securities-symbol-edit",
    ),
    path(
        "settings/securities-symbols/<int:id>/delete",
        settings.securities_symbol_delete,
        name="settings-securities-symbol-delete",
    ),
    # lab
    path("lab/", lab.index, name="lab"),
    path("lab/email", lab.email_test, name="email-test"),
    path("lab/sms/", lab.sms_test, name="sms-test"),
]

urlpatterns += staticfiles_urlpatterns()
