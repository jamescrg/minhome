
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from apps.tasks.models import Task
from apps.tasks.forms import TaskForm
from apps.folders.models import Folder


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
def activate(request, id):
    Folder.objects.filter(user_id=1, active=1).update(active=0)
    folder = get_object_or_404(Folder, pk=id)
    folder.active = 1
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
def add(request):

    if request.method == 'POST':
        task = Task()
        task.user_id = request.user.id
        folder = get_object_or_404(Folder, pk=request.POST.get('folder_id'))
        task.folder = folder
        task.title = request.POST.get('title')
        task.save()
        return redirect('tasks')


@login_required
def edit(request, id):

    user_id = request.user.id

    if request.method == 'POST':

        try:
            task = Task.objects.filter(user_id=request.user.id, pk=id).get()
        except ObjectDoesNotExist:
            raise Http404('Record not found.')

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_id = user_id
            task.save()

        return redirect('tasks')

    else:

        task = get_object_or_404(Task, pk=id)
        folders = Folder.objects.filter(user_id=user_id, page='tasks').order_by('name')
        selected_folder = folders.filter(id=task.folder.id).get()

        form = TaskForm(instance=task, initial={'folder': selected_folder.id})
        form.fields['folder'].queryset = Folder.objects.filter(
                user_id=user_id, page='tasks').order_by('name')

        context = {
            'page': 'tasks',
            'edit': True,
            'folders': folders,
            'action': f'/tasks/{id}/edit',
            'form': form,
        }

        return render(request, 'tasks/content.html', context)


@login_required
def clear(request, folder_id):
    user_id = request.user.id
    tasks = Task.objects.filter(user_id=user_id, folder_id=folder_id, status=1)
    for task in tasks:
        task.delete()
    return redirect('/tasks/')
