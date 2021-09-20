
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import Http404
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
    selected_folders = folders.filter(selected=1).order_by('-active', 'name')
    active_folder = folders.filter(user_id=user_id, active=1).first()

    if selected_folders:
        for folder in selected_folders:
            tasks = Task.objects.filter(folder_id=folder.id)
            tasks = tasks.order_by('status', 'title')
            folder.tasks = tasks

    context = {
        'page': page,
        'folders': folders,
        'active_folder': active_folder,
        'selected_folders': selected_folders,
    }

    return render(request, 'tasks/content.html', context)

@login_required
def activate(request,id):
    Folder.objects.filter(user_id=1, active=1).update(active=0)
    folder = get_object_or_404(Folder, pk=id)
    folder.active=1
    folder.save()
    return redirect('/tasks/')

@login_required
def status(request, id):
    task = get_object_or_404(Task, pk=id)
    if task.status == 1:
        task.status = 0
    else: 
        task.status = 1
    task.save()
    return redirect('/tasks/')

@login_required
def insert(request):
    task = Task()
    task.user_id = request.user.id
    task.folder_id = request.POST.get('folder_id')
    task.title = request.POST.get('title')
    task.save()
    return redirect('tasks')

@login_required
def edit(request, id):
    user_id = request.user.id
    task = get_object_or_404(Task, pk=id)
    folders = Folder.objects.filter(user_id=user_id, page='tasks').order_by('name')
    selected_folder_id = task.folder_id
    selected_folder = get_object_or_404(Folder, pk=selected_folder_id)
    context = {
        'page': 'tasks',
        'edit': True,
        'action': f'/tasks/update/{id}',
        'folders': folders,
        'selected_folder': selected_folder,
        'selected_folder_id': selected_folder_id,
        'task': task,
    }
    return render(request, 'tasks/content.html', context)

@login_required
def update(request, id):
    try:
        task = Task.objects.filter(user_id=request.user.id, pk=id).get()
    except:
        raise Http404('Record not found.')
    task.user_id = request.user.id
    task.folder_id = request.POST.get('folder_id')
    task.title = request.POST.get('title')
    task.save()
    return redirect('tasks')

@login_required
def clear(request, folder_id):
    user_id = request.user.id
    tasks = Task.objects.filter(user_id=user_id, folder_id=folder_id, status=1)
    for task in tasks:
        task.delete()
    return redirect('/tasks/')
