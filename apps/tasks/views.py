from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from apps.folders.folders import get_task_folders, select_folders
from apps.folders.models import Folder
from apps.tasks.forms import TaskForm
from apps.tasks.models import Task


@login_required
def index(request):
    """Display a list of folders and one or more lists of tasks.

    Notes:
        * Always displays folders.
        * If a folder is selected, displays the tasks for that folder.
        * Allows the display of mulitple task folders.
        * Task folders are informally called "lists" but are part of the consolidated
          folder system for the whole site.
    """

    folders = get_task_folders(request)

    selected_folders = select_folders(request, "tasks")

    active_folder_id = request.user.tasks_active_folder

    if active_folder_id:
        active_folder = get_object_or_404(Folder, pk=active_folder_id)
    else:
        active_folder = None

    if selected_folders:
        for folder in selected_folders:
            tasks = Task.objects.filter(folder_id=folder.id)
            tasks = tasks.order_by("status", "title")
            folder.tasks = tasks

    if active_folder:
        active_folder.tasks = Task.objects.filter(folder_id=active_folder.id).order_by(
            "status", "title"
        )

    context = {
        "page": "tasks",
        "folders": folders,
        "selected_folders": selected_folders,
        "active_folder": active_folder,
    }

    return render(request, "tasks/content.html", context)


@login_required
def activate(request, id):
    """Activate a folder.

    Notes:
        This makes the folder the "active" folder for task entry.
        That means that new tasks created on the task page are added to this folder.
    """

    user = request.user
    user.tasks_active_folder = id
    user.save()
    return redirect("/tasks/")


@login_required
def status(request, id, origin="tasks"):
    """Update a task status to complete / not complete

    Args:
        id (int): a task id
        origin (str): the page from which the request originated and should return

    Notes:
        Tasks may be updated from the home or the task page,
        in which case, the user should be returned to the page of origin.
    """

    task = get_object_or_404(Task, pk=id)
    if task.status == 1:
        task.status = 0
    else:
        task.status = 1
    task.save()
    return redirect(origin)


@login_required
def add(request):
    """Add a new task.

    Notes:
        GET: There is no get method for this view.
             The task form is always visible via "index".
        POST: Add task to database.
    """

    if request.method == "POST":
        task = Task()
        task.user = request.user
        folder = get_object_or_404(Folder, pk=request.POST.get("folder_id"))
        task.folder = folder
        task.title = request.POST.get("title")
        task.title = task.title[0].upper() + task.title[1:]
        task.save()
        return redirect("tasks")


@login_required
def edit(request, id):
    """Edit a task.

    Args:
        id (int): A Task instance id

    Notes:
        GET: Display task edit form.
        POST: Update task in database.
    """

    user = request.user

    if request.method == "POST":
        try:
            task = Task.objects.filter(pk=id).get()
        except ObjectDoesNotExist:
            raise Http404("Record not found.")

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.title = task.title[0].upper() + task.title[1:]
            task.save()

        return redirect("tasks")

    else:
        task = get_object_or_404(Task, pk=id)
        folders = get_task_folders(request)
        selected_folder = folders.filter(id=task.folder.id).get()

        form = TaskForm(instance=task, initial={"folder": selected_folder.id})
        form.fields["folder"].queryset = folders

        context = {
            "page": "tasks",
            "edit": True,
            "folders": folders,
            "action": f"/tasks/{id}/edit",
            "form": form,
        }

        return render(request, "tasks/content.html", context)


@login_required
def clear(request, folder_id):
    """Delete all completed tasks in the active folder.

    Args:
        folder_id (int): the folder where tasks should be deleted
    """

    tasks = Task.objects.filter(folder_id=folder_id, status=1)
    for task in tasks:
        task.delete()
    return redirect("/tasks/")
