from django.contrib import admin
from django.urls import path, include
from app import views_home
from app import views_favorites
from app import views_tasks
from app import views_contacts
from app import views_notes
from app import views_search
from app import views_settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_home.index, name='home'),
    path('home/', views_home.index, name='home'),
    path('favorites/', views_favorites.index, name='favorites'),
    path('tasks/', views_tasks.index, name='tasks'),
    path('contacts/', views_contacts.index, name='contacts'),
    path('notes/', views_notes.index, name='notes'),
    path('search/', views_search.index, name='search'),
    path('settings/', views_settings.index, name='settings'),
]
