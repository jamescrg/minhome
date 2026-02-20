from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    # List views
    path("", views.notes_index, name="index"),
    path("list/", views.notes_list, name="list"),
    path("all/", views.notes_all, name="all"),
    path("add/", views.notes_add, name="add"),
    path("order-by/<str:order>/", views.notes_order_by, name="order-by"),
    path("filter/keyword/", views.notes_filter_keyword, name="filter-keyword"),
    path("bulk-delete/", views.notes_bulk_delete, name="bulk-delete"),
    path("bulk-move-folder/", views.notes_bulk_move_folder, name="bulk-move-folder"),
    # Editor views
    path("<int:note_id>/", views.note_view, name="note-view"),
    path(
        "<int:note_id>/content-partial/",
        views.note_content_partial,
        name="note-content-partial",
    ),
    path("<int:note_id>/edit/", views.note_edit, name="edit"),
    path("<int:note_id>/delete/", views.note_delete, name="delete"),
    path("<int:note_id>/autosave/", views.note_autosave, name="note-autosave"),
    path("<int:note_id>/title/", views.note_title, name="note-title"),
    path(
        "<int:note_id>/sidebar/sort/<str:sort_key>/",
        views.sidebar_sort,
        name="note-sidebar-sort",
    ),
    path("shortcuts/", views.notes_shortcuts, name="notes-shortcuts"),
    path(
        "<int:note_id>/import-modal/",
        views.note_import_modal,
        name="note-import-modal",
    ),
]
