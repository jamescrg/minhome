from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Folder, Task
from pprint import pprint

@login_required
def index(request):

    user_id = request.user.id
    page = 'tasks'

    folders = Folder.objects.filter(user_id=user_id, page=page).order_by('name')

    selected_folders = folders.filter(selected=1, active=0)
    active_folder = folders.filter(active=1).first()

    if selected_folders:
        for folder in selected_folders:
            tasks = Task.objects.filter(folder_id=folder.id)
            tasks = tasks.order_by('status').order_by('title')
            folder.tasks = tasks

    if active_folder:
        tasks = Task.objects.filter(folder_id=active_folder.id)
        active_folder.tasks = tasks.order_by('status').order_by('title')

    context = {
        'page': page,
        'folders': folders,
        'selected_folders': selected_folders,
        'active_folder': active_folder,
    }

    return render(request, 'tasks/content.html', context)


def create(request, id):
    user_id = request.user.id
    selected_folder_id = id
    selected_folder = get_object_or_404(Folder, pk=id)
    folders = Folder.objects.filter(user_id=user_id, page='favorites').order_by('name')
    favorite = Favorite()
    favorite.folder_id = id

    context = {
        'page': 'favorites',
        'edit': False,
        'add': True,
        'action': '/favorites/insert',
        'folders': folders,
        'selected_folder': selected_folder,
        'selected_folder_id': selected_folder_id,
        'favorite': favorite,
    }

    return render(request, 'favorites/content.html', context)


def insert(request):
    favorite = Favorite()
    favorite.user_id = request.user.id
    for field in favorite.fillable:
         setattr(favorite, field, request.POST.get(field))
    favorite.save()
    return redirect('favorites')


def edit(request, id):
    user_id = request.user.id
    favorite = get_object_or_404(Favorite, pk=id)
    folders = Folder.objects.filter(user_id=user_id, page='favorites').order_by('name')
    selected_folder_id = favorite.folder_id
    selected_folder = get_object_or_404(Folder, pk=selected_folder_id)

    context = {
        'page': 'favorites',
        'edit': True,
        'add': False,
        'action': f'/favorites/update/{id}',
        'folders': folders,
        'selected_folder': selected_folder,
        'selected_folder_id': selected_folder_id,
        'favorite': favorite,
    }


    return render(request, 'favorites/content.html', context)


def update(request, id):
    favorite = get_object_or_404(Favorite, pk=id)
    for field in favorite.fillable:
         setattr(favorite, field, request.POST.get(field))
    favorite.save()
    return redirect('favorites')


def delete(request, id):
    favorite = get_object_or_404(Favorite, pk=id)
    favorite.delete()
    return redirect('favorites')


def home(request, id):
    user_id = request.user.id
    favorite = get_object_or_404(Favorite, pk=id)
    if favorite.home_rank: 
        favorite.home_rank = 0
    else: 
        favorite.home_rank = 1
    
    favorite.save()
    return redirect('favorites')
