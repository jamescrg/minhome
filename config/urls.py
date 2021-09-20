from django.contrib import admin
from django.urls import path, include

from app import views_folders
from app import views_home
from app import views_favorites
from app import views_tasks
from app import views_contacts
from app import views_notes
from app import views_search
from app import views_settings
from app import views_weather


urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # folders
    path('folders/home/<int:id>/<str:page>', views_folders.home, name='folder-home'),
    path('folders/<int:id>/<str:page>', views_folders.select, name='folder-select'),
    path('folders/insert/<str:page>', views_folders.insert, name='folder-insert'),
    path('folders/update/<int:id>/<str:page>', views_folders.update, name='folder-update'),
    path('folders/delete/<int:id>/<str:page>', views_folders.delete, name='folder-delete'),

    # home
    path('', views_home.index, name='home-index'),
    path('home/', views_home.index, name='home'),
    path('home/folder/<int:id>/<str:direction>/', views_home.folder, name='home-folder'),
    path('home/favorite/<int:id>/<str:direction>/', 
        views_home.favorite, name='home-favorite'),

    # favorites
    path('favorites/', views_favorites.index, name='favorites'),
    path('favorites/add/<int:id>', views_favorites.add, name='favorites-add'),
    path('favorites/insert', views_favorites.insert, name='favorites-insert'),
    path('favorites/edit/<int:id>', views_favorites.edit, name='favorites-edit'),
    path('favorites/update/<int:id>', views_favorites.update, name='favorites-update'),
    path('favorites/delete/<int:id>', views_favorites.delete, name='favorites-delete'),
    path('favorites/home/<int:id>', views_favorites.home, name='favorites-home'),

    # tasks
    path('tasks/', views_tasks.index, name='tasks'),
    path('tasks/edit/<int:id>', views_tasks.edit,  name='tasks-edit'),
    path('tasks/activate/<int:id>', views_tasks.activate, name='tasks-activate'),
    path('tasks/complete/<int:id>', views_tasks.status, name='tasks-complete'),
    path('tasks/clear/<int:folder_id>', views_tasks.clear, name='tasks-clear'),
    path('tasks/insert', views_tasks.insert, name='tasks-insert'),
    path('tasks/update/<int:id>', views_tasks.update, name='tasks-update'),
    
    # contacts
    path('contacts/', views_contacts.index, name='contacts'),
    path('contacts/add/<int:id>', views_contacts.add, name='contacts-add'),
    path('contacts/edit/<int:id>', views_contacts.edit, name='contacts-edit'),
    path('contacts/<int:id>', views_contacts.select, name='contacts-select'),
    path('contacts/insert', views_contacts.insert, name='contacts-insert'),
    path('contacts/update/<int:id>', views_contacts.update, name='contacts-update'),
    path('contacts/delete/<int:id>', views_contacts.delete, name='contacts-delete'),
    path('contacts/google/<int:id>', views_contacts.google_sync, name='contacts-google'),

    # notes
    path('notes/', views_notes.index, name='notes'),
    path('notes/add/<int:id>', views_notes.add, name='notes-add'),
    path('notes/<int:id>', views_notes.select, name='notes-select'),
    path('notes/edit/<int:id>', views_notes.edit, name='notes-edit'),
    path('notes/insert', views_notes.insert, name='notes-insert'),
    path('notes/update/<int:id>', views_notes.update, name='notes-update'),
    path('notes/delete/<int:id>', views_notes.delete, name='notes-delete'),

    # weather
    path('weather/', views_weather.index, name='weather'),

    # search
    path('search/', views_search.index, name='search'),
    path('search/results', views_search.results, name='search-results'),

    # settings
    path('settings/', views_settings.index, name='settings'),
    path('settings/google/login', views_settings.google_login, name='settings-google-login'),
    path('settings/google/store', views_settings.google_store, name='settings-google-store'),
    path('settings/google/logout', views_settings.google_logout, name='settings-google-logout'),

]
