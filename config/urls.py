from django.contrib import admin
from django.urls import path, include

from apps.folders import views as folders
from apps.home import views as home
from apps.favorites import views as favorites
from apps.tasks import views as tasks
from apps.contacts import views as contacts
from apps.notes import views as notes
from apps.search import views as search
from apps.settings import views as settings
from apps.finance import views as finance
from apps.weather import views as weather


urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # folders
    path('folders/home/<int:id>/<str:page>', folders.home, name='folder-home'),
    path('folders/<int:id>/<str:page>', folders.select, name='folder-select'),
    path('folders/insert/<str:page>', folders.insert, name='folder-insert'),
    path('folders/update/<int:id>/<str:page>', folders.update, name='folder-update'),
    path('folders/delete/<int:id>/<str:page>', folders.delete, name='folder-delete'),

    # home
    path('', home.index, name='home-index'),
    path('home/', home.index, name='home'),
    path('home/folder/<int:id>/<str:direction>/', home.folder, name='home-folder'),
    path('home/favorite/<int:id>/<str:direction>/', 
        home.favorite, name='home-favorite'),

    # favorites
    path('favorites/', favorites.index, name='favorites'),
    path('favorites/add/<int:id>', favorites.add, name='favorites-add'),
    path('favorites/insert', favorites.insert, name='favorites-insert'),
    path('favorites/edit/<int:id>', favorites.edit, name='favorites-edit'),
    path('favorites/update/<int:id>', favorites.update, name='favorites-update'),
    path('favorites/delete/<int:id>', favorites.delete, name='favorites-delete'),
    path('favorites/home/<int:id>', favorites.home, name='favorites-home'),

    # tasks
    path('tasks/', tasks.index, name='tasks'),
    path('tasks/edit/<int:id>', tasks.edit,  name='tasks-edit'),
    path('tasks/activate/<int:id>', tasks.activate, name='tasks-activate'),
    path('tasks/complete/<int:id>', tasks.status, name='tasks-complete'),
    path('tasks/clear/<int:folder_id>', tasks.clear, name='tasks-clear'),
    path('tasks/insert', tasks.insert, name='tasks-insert'),
    path('tasks/update/<int:id>', tasks.update, name='tasks-update'),
    
    # contacts
    path('contacts/', contacts.index, name='contacts'),
    path('contacts/add/<int:id>', contacts.add, name='contacts-add'),
    path('contacts/edit/<int:id>', contacts.edit, name='contacts-edit'),
    path('contacts/<int:id>', contacts.select, name='contacts-select'),
    path('contacts/insert', contacts.insert, name='contacts-insert'),
    path('contacts/update/<int:id>', contacts.update, name='contacts-update'),
    path('contacts/delete/<int:id>', contacts.delete, name='contacts-delete'),
    path('contacts/google/<int:id>', contacts.google_sync, name='contacts-google'),

    # notes
    path('notes/', notes.index, name='notes'),
    path('notes/newform/', notes.new_form, name='notes-newform'),
    path('notes/add/<int:id>', notes.add, name='notes-add'),
    path('notes/<int:id>', notes.select, name='notes-select'),
    path('notes/edit/<int:id>', notes.edit, name='notes-edit'),
    path('notes/insert', notes.insert, name='notes-insert'),
    path('notes/update/<int:id>', notes.update, name='notes-update'),
    path('notes/delete/<int:id>', notes.delete, name='notes-delete'),

    # weather
    path('weather/', weather.index, name='weather'),

    # finance
    path('crypto/', finance.crypto, name='crypto'),
    path('crypto/<str:ord>', finance.crypto, name='crypto'),
    path('securities/', finance.securities, name='securities'),

    # search
    path('search/', search.index, name='search'),
    path('search/results', search.results, name='search-results'),

    # settings
    path('settings/', settings.index, name='settings'),
    path('settings/google/login', settings.google_login, name='settings-google-login'),
    path('settings/google/store', settings.google_store, name='settings-google-store'),
    path('settings/google/logout', settings.google_logout, name='settings-google-logout'),

]
