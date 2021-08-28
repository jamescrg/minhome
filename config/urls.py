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

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # folders
    path('folders/home/<int:id>/<str:page>', views_folders.home, name='folder-home'),
    path('folders/<int:id>/<str:page>', views_folders.select, name='folder-select'),
    path('folders/create/<str:page>', views_folders.insert, name='folder-insert'),
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
    path('favorites/create/<int:id>', views_favorites.create, name='favorites-add'),
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
    path('contacts/create/<int:id>', views_contacts.create, name='contacts-create'),
    # path('contacts/edit/<int:id>', views_contacts.edit, name=''),
    path('contacts/<int:id>', views_contacts.select, name='contacts-select'),
    # path('contacts', views_contacts.store, name=''),
    # path('contacts/update/<int:id>', views_contacts.update, name=''),
    # path('contacts/delete/<int:id>', views_contacts.destroy, name=''),

    # notes
    path('notes/', views_notes.index, name='notes'),
    # path('notes/create/<int:id>', views_notes.create, name=''),
    # path('notes/<int:id>', views_notes.show, name=''),
    # path('notes/edit/<int:id>', views_notes.edit, name=''),
    # path('notes', views_notes.store, name=''),
    # path('notes/update/<int:id>', views_notes.update, name=''),
    # path('notes/delete/<int:id>', views_notes.destroy, name=''),

    # search
    path('search/', views_search.index, name='search'),
    # path('search', views_search.search, name=''),

    # settings
    path('settings/', views_settings.index, name='settings'),
    # path('settings/google/login', views_settings.googleLogin, name=''),
    # path('settings/google/store', views_settings.googleStore, name=''),
    # path('settings/google/logout', views_settings.googleLogout, name=''),

]
